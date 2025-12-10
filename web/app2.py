import streamlit as st
from collections import deque, defaultdict
from pathlib import Path
import heapq

st.set_page_config(page_title="Flight Management System (FMS)", layout="wide")

if "role" not in st.session_state:
    st.session_state.role = "User"

header_left, header_right = st.columns([3, 1])
with header_left:
    st.title("Flight Management System")
with header_right:
    st.selectbox("Role", ["User", "Admin"], key="role")

# ---------- Simple file-based DB ----------
DB_PATH = Path(__file__).with_name("flights_db.txt")


def load_flights_from_db():
    flights = []
    if not DB_PATH.exists():
        return flights
    with DB_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 6:
                continue
            fid, src, dst, dist_str, seats_str, active_str = [p.strip() for p in parts]
            try:
                dist = int(dist_str)
                seats = int(seats_str)
            except ValueError:
                continue
            active = active_str.lower() == "true"
            flights.append({
                "flightID": fid,
                "source": src,
                "destination": dst,
                "distance": dist,
                "seats": seats,
                "active": active,
                "bookings": [],
            })
    return flights


def save_flights_to_db():
    lines = []
    for f in st.session_state.flights:
        line = f"{f['flightID']},{f['source']},{f['destination']},{f['distance']},{f['seats']},{str(f['active'])}"
        lines.append(line)
    with DB_PATH.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------- Session state init ----------
if "flights" not in st.session_state:
    loaded = load_flights_from_db()
    if loaded:
        st.session_state.flights = loaded
    else:
        st.session_state.flights = [
            {"flightID": "F101", "source": "Pune", "destination": "Mumbai", "distance": 150, "seats": 5, "active": True, "bookings": []},
            {"flightID": "F102", "source": "Delhi", "destination": "Mumbai", "distance": 1400, "seats": 3, "active": True, "bookings": []},
            {"flightID": "F103", "source": "Pune", "destination": "Bangalore", "distance": 840, "seats": 2, "active": True, "bookings": []},
        ]
        save_flights_to_db()
if "flight_index" not in st.session_state:
    st.session_state.flight_index = {f["flightID"]: idx for idx, f in enumerate(st.session_state.flights)}
if "booking_queue" not in st.session_state:
    st.session_state.booking_queue = deque()  
if "global_booking_id" not in st.session_state:
    st.session_state.global_booking_id = 1
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []  
if "graph" not in st.session_state:
    st.session_state.graph = defaultdict(list)


def rebuild_graph():
    g = defaultdict(list)
    for f in st.session_state.flights:
        if not f["active"]:
            continue
        src = f["source"]
        dst = f["destination"]
        dist = f["distance"]
        g[src].append((dst, dist))
        g[dst].append((src, dist))
    st.session_state.graph = g

def rebuild_index():
    st.session_state.flight_index = {f["flightID"]: idx for idx, f in enumerate(st.session_state.flights)}

def add_flight_params(fid, src, dst, dist, seats):
    if fid in st.session_state.flight_index:
        return False, "Flight ID already exists."
    if len(st.session_state.flights) >= 100:
        return False, "Max flights reached."
    f = {"flightID": fid, "source": src, "destination": dst, "distance": dist, "seats": seats, "active": True, "bookings": []}
    st.session_state.flights.append(f)
    st.session_state.flight_index[fid] = len(st.session_state.flights) - 1
    rebuild_graph()
    save_flights_to_db()
    return True, "Added"

def list_flights():
    return st.session_state.flights


def cancel_flight(fid):
    idx = st.session_state.flight_index.get(fid)
    if idx is None:
        return False, "Flight not found."
    f = st.session_state.flights[idx]
    if not f["active"]:
        return False, "Flight is already cancelled."
    f["active"] = False
    rebuild_graph()
    save_flights_to_db()
    return True, f"Flight {fid} cancelled."


def schedule_flight(fid):
    idx = st.session_state.flight_index.get(fid)
    if idx is None:
        return False, "Flight not found."
    f = st.session_state.flights[idx]
    if f["active"]:
        return False, "Flight is already active."
    f["active"] = True
    rebuild_graph()
    save_flights_to_db()
    return True, f"Flight {fid} scheduled / activated."

def queue_booking(fid, passenger):
    idx = st.session_state.flight_index.get(fid)
    if idx is None:
        return False
    f = st.session_state.flights[idx]
    if not f["active"]:
        return False
    st.session_state.booking_queue.append(fid)
    return True

def process_next_booking_noninteractive(passenger_name):
    if not st.session_state.booking_queue:
        return False, "No bookings in queue."
    fid = st.session_state.booking_queue.popleft()
    idx = st.session_state.flight_index.get(fid)
    if idx is None:
        return False, f"Flight {fid} not found."
    f = st.session_state.flights[idx]
    if not f["active"]:
        return False, f"Flight {fid} is cancelled."
    if f["seats"] <= 0:
        return False, f"No seats left on {fid}."
    # assign booking
    bid = st.session_state.global_booking_id
    st.session_state.global_booking_id += 1
    f["bookings"].append((bid, passenger_name))
    f["seats"] -= 1
    return True, f"Booking confirmed for {passenger_name} on {fid}, booking id {bid}."

def get_bookings_for_flight(fid):
    idx = st.session_state.flight_index.get(fid)
    if idx is None:
        return []
    return st.session_state.flights[idx]["bookings"]

def cancel_booking_by_id(fid, booking_id):
    idx = st.session_state.flight_index.get(fid)
    if idx is None:
        return False
    f = st.session_state.flights[idx]
    for i, (bid, name) in enumerate(f["bookings"]):
        if bid == booking_id:
            f["bookings"].pop(i)
            f["seats"] += 1
            return True
    return False

def search_flights_by_source_noninteractive(src):
    src_norm = src.strip().lower()
    res = []
    if not src_norm:
        for f in st.session_state.flights:
            if f["active"]:
                res.append(f)
    else:
        for f in st.session_state.flights:
            if f["source"].lower() == src_norm and f["active"]:
                res.append(f)
    if src_norm:
        st.session_state.recent_searches.append(src_norm)
    return res

def recent_searches_list():
    return list(reversed(st.session_state.recent_searches))  # top first


def list_booking_queue():
    return list(st.session_state.booking_queue)

# Graph algorithms (Dijkstra, DFS, BFS, Prim, Kruskal)
def dijkstra_path(src, dest):
    graph = st.session_state.graph
    if src not in graph or dest not in graph:
        return None, []
    # standard Dijkstra
    pq = [(0, src)]
    dist = {src: 0}
    parent = {src: None}
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == dest:
            break
        for v, w in graph[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    if dest not in dist:
        return None, []
    # reconstruct path
    path = []
    cur = dest
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return dist[dest], path

def dfs(start):
    graph = st.session_state.graph
    visited = set()
    order = []
    def _dfs(u):
        visited.add(u)
        order.append(u)
        for v, _ in graph[u]:
            if v not in visited:
                _dfs(v)
    if start not in graph:
        return []
    _dfs(start)
    return order

def bfs(start):
    graph = st.session_state.graph
    if start not in graph:
        return []
    q = deque([start])
    visited = {start}
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in graph[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
    return order

def prim_mst(start):
    graph = st.session_state.graph
    if start not in graph:
        return [], 0
    visited = set([start])
    edges = []
    total = 0
    pq = []
    for v, w in graph[start]:
        heapq.heappush(pq, (w, start, v))
    while pq:
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue
        visited.add(v)
        edges.append((u, v, w))
        total += w
        for nx, nw in graph[v]:
            if nx not in visited:
                heapq.heappush(pq, (nw, v, nx))
    return edges, total

def kruskal_mst():
    # build edges unique u<v
    graph = st.session_state.graph
    nodes = list(graph.keys())
    idx = {n:i for i,n in enumerate(nodes)}
    edges = []
    for u in graph:
        for v,w in graph[u]:
            if idx[u] < idx[v]:
                edges.append((w, u, v))
    edges.sort()
    parent = {n:n for n in nodes}
    rank = {n:0 for n in nodes}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    def union(a,b):
        ra, rb = find(a), find(b)
        if ra==rb: return False
        if rank[ra]<rank[rb]:
            parent[ra]=rb
        else:
            parent[rb]=ra
            if rank[ra]==rank[rb]: rank[ra]+=1
        return True
    mst = []
    total = 0
    for w,u,v in edges:
        if union(u,v):
            mst.append((u,v,w))
            total += w
    return mst, total

with st.sidebar:
    st.header("Dashboard")
    total_flights = len(st.session_state.flights)
    active_flights = sum(1 for f in st.session_state.flights if f["active"])
    total_bookings = sum(len(f["bookings"]) for f in st.session_state.flights)
    st.metric("Total confirmed bookings", total_bookings)

role = st.session_state.role

if role == "Admin":
    (tab_flights,) = st.tabs(["Flights (Admin)"])
else:
    tab_bookings, tab_search, tab_graph = st.tabs([
        "Bookings (User)",
        "Search",
        "Graphs & MST",
    ])

if role == "Admin":
    with tab_flights:
        st.subheader("Manage flights")
        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("### Add flight")
            with st.form("add_flight_form"):
                fid = st.text_input("Flight ID", value="F104")
                src = st.text_input("Source", value="Pune")
                dst = st.text_input("Destination", value="Goa")
                dist = st.number_input("Distance (km)", min_value=1, value=400)
                seats = st.number_input("Seats", min_value=1, value=10)
                submitted = st.form_submit_button("Add flight")
                if submitted:
                    ok, msg = add_flight_params(fid.strip(), src.strip(), dst.strip(), int(dist), int(seats))
                    if ok:
                        st.success(f"Added flight {fid}")
                    else:
                        st.error(msg)

        with col2:
            st.markdown("### Flights overview")
            flights = list_flights()
            if not flights:
                st.write("No flights added yet.")
            else:
                rows = []
                for f in flights:
                    rows.append({
                        "FlightID": f["flightID"],
                        "Source": f["source"],
                        "Destination": f["destination"],
                        "Distance": f["distance"],
                        "Seats": f["seats"],
                        "Active": f["active"]
                    })
                st.table(rows)

        st.markdown("### Change flight status")
        ccol1, ccol2 = st.columns(2)
        with ccol1:
            cfid = st.text_input("Flight ID to cancel", key="cancel_fid")
            if st.button("Cancel flight", key="cancel_fid_btn"):
                ok, msg = cancel_flight(cfid.strip())
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
        with ccol2:
            sfid = st.text_input("Flight ID to schedule / activate", key="schedule_fid")
            if st.button("Schedule / activate flight", key="schedule_fid_btn"):
                ok, msg = schedule_flight(sfid.strip())
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

if role == "User":
    with tab_bookings:
        st.subheader("Booking operations")
        bcol1, bcol2, bcol3 = st.columns(3)

        with bcol1:
            st.markdown("### Queue booking")
            with st.form("queue_booking"):
                bid_fid = st.text_input("Flight ID to queue", value="")
                passenger = st.text_input("Passenger name", value="Alice")
                queued = st.form_submit_button("Queue booking")
                if queued:
                    ok = queue_booking(bid_fid.strip(), passenger.strip())
                    if ok:
                        st.success(f"Queued booking for {passenger} on {bid_fid}")
                    else:
                        st.error("Failed to queue booking — flight not found/active.")

        with bcol2:
            st.markdown("### Process next booking")
            pname = st.text_input("Passenger name to assign when processing", value="AssignedPassenger")
            if st.button("Process next booking"):
                ok, msg = process_next_booking_noninteractive(pname.strip())
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

        with bcol3:
            st.markdown("### Show bookings for a flight")
            fid_q = st.text_input("Flight ID to show bookings", value="")
            if st.button("Show bookings"):
                bookings = get_bookings_for_flight(fid_q.strip())
                if not bookings:
                    st.write("No bookings.")
                else:
                    st.table([{"BookingId": b[0], "Passenger": b[1]} for b in bookings])

            st.markdown("### Cancel booking by ID")
            cb_fid = st.text_input("Flight ID (cancel)", value="", key="cb_fid")
            cb_bid = st.number_input("Booking ID", min_value=1, value=1, key="cb_bid")
            if st.button("Cancel booking", key="cb_btn"):
                ok = cancel_booking_by_id(cb_fid.strip(), int(cb_bid))
                if ok:
                    st.success("Booking cancelled.")
                else:
                    st.error("Booking not found for given flight / ID.")

        st.markdown("### Pending booking queue")
        queue = list_booking_queue()
        if not queue:
            st.write("No bookings currently in queue.")
        else:
            st.table([{"Position": i + 1, "FlightID": fid} for i, fid in enumerate(queue)])

    with tab_search:
        st.subheader("Search flights & recent searches")
        gcol1, gcol2 = st.columns(2)
        with gcol1:
            st.markdown("### Search flights by source")
            src_q = st.text_input("Source", value="")
            if st.button("Search by source"):
                results = search_flights_by_source_noninteractive(src_q.strip())
                if not results:
                    st.write("No flights found.")
                else:
                    st.table([{"FlightID": f["flightID"], "To": f["destination"], "Distance": f["distance"], "Seats": f["seats"]} for f in results])

        with gcol2:
            st.markdown("### Recent searches")
            if st.button("Show recent searches"):
                rs = recent_searches_list()
                if not rs:
                    st.write("No recent searches.")
                else:
                    st.write(", ".join(rs))

    with tab_graph:
        st.subheader("Graph algorithms")
        gcol1, gcol2 = st.columns(2)

        with gcol1:
            st.markdown("### Shortest path (Dijkstra)")
            src = st.text_input("Source airport", value="")
            dst = st.text_input("Destination airport", value="")
            if st.button("Find shortest path"):
                dist, path = dijkstra_path(src.strip(), dst.strip())
                if dist is None:
                    st.error("No path found or airports not in graph.")
                else:
                    st.success(f"Distance = {dist}")
                    st.write("Path: " + " -> ".join(path))

            st.markdown("### DFS / BFS")
            dfs_start = st.text_input("DFS start", value="")
            bfs_start = st.text_input("BFS start", value="")
            if st.button("Run DFS"):
                order = dfs(dfs_start.strip())
                if not order:
                    st.error("Start airport not in graph.")
                else:
                    st.write("DFS order: " + " -> ".join(order))
            if st.button("Run BFS"):
                order = bfs(bfs_start.strip())
                if not order:
                    st.error("Start airport not in graph.")
                else:
                    st.write("BFS order: " + " -> ".join(order))

        with gcol2:
            st.markdown("### MST (Prim / Kruskal)")
            prim_start = st.text_input("Prim start", value="")
            if st.button("Prim MST"):
                edges, total = prim_mst(prim_start.strip())
                if not edges:
                    st.error("Prim start not in graph or not enough nodes.")
                else:
                    st.write("Edges:")
                    for u, v, w in edges:
                        st.write(f"{u} - {v} ({w})")
                    st.write(f"Total MST weight = {total}")
            if st.button("Kruskal MST"):
                edges, total = kruskal_mst()
                if not edges:
                    st.error("Not enough nodes for MST.")
                else:
                    st.write("Edges:")
                    for u, v, w in edges:
                        st.write(f"{u} - {v} ({w})")
                st.write(f"Total MST weight = {total}")

rebuild_graph()
