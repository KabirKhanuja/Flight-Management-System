import streamlit as st
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python_package"))
sys.path.insert(0, str(ROOT / "cpp_bindings"))

from flight_fms import api, flight_fms_cpp

st.set_page_config(page_title="Flight Management System (FMS)", layout="wide")

st.title("Flight Management System — Streamlit UI")

NONINTERACTIVE = api.is_noninteractive_ready()

if NONINTERACTIVE:
    st.success("Non-interactive C++ bindings detected. UI will call C++ methods directly.")
else:
    st.warning("Non-interactive C++ bindings not found. The UI will show fallback options. "
               "Build and install the updated pybind11 extension with non-interactive wrappers to enable full functionality.")


with st.sidebar:
    st.header("Status & Actions")
    if NONINTERACTIVE:
        st.write("Backend: non-interactive pybind11 extension loaded.")
    else:
        st.write("Backend: interactive-only extension or not built.")
        if st.button("Build extension (scripts/build_extension.sh)"):
            st.info("Please run `scripts/build_extension.sh` in your terminal. This web process cannot run builds automatically.")
    st.markdown("---")
    st.write("Developer notes:")
    st.write("- If you add non-interactive wrappers (add_flight_params, listFlights, etc.) rebuild extension.")
    st.write("- CLI fallback uses compiled `fms_app` executable (CMake build).")

st.markdown("## Flights")

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Add flight")
    if NONINTERACTIVE:
        with st.form("add_flight_form"):
            fid = st.text_input("Flight ID", value="F101")
            src = st.text_input("Source", value="Pune")
            dst = st.text_input("Destination", value="Mumbai")
            dist = st.number_input("Distance (km)", min_value=1, value=300)
            seats = st.number_input("Seats", min_value=1, value=100)
            submitted = st.form_submit_button("Add flight")
            if submitted:
                ok = flight_fms_cpp._fs.addFlightParams(fid, src, dst, int(dist), int(seats)) if hasattr(flight_fms_cpp._fs, "addFlightParams") else None
                if ok is True:
                    st.success(f"Added flight {fid}")
                elif ok is False:
                    st.error("Failed to add flight (maybe full).")
                else:
                    st.error("Non-interactive wrapper not available. Build updated bindings.")
    else:
        st.info("Non-interactive add flight not available. You can either:\n\n"
                "1. Build non-interactive bindings (recommended), or\n"
                "2. Use the CLI (compile the CMake `fms_app`) and run it manually.")

with col2:
    st.subheader("Active flights")
    if NONINTERACTIVE and hasattr(flight_fms_cpp._fs, "listFlights"):
        try:
            flights = flight_fms_cpp._fs.listFlights()
            if not flights:
                st.write("No flights added yet.")
            else:
                rows = []
                for f in flights:
                    rows.append({
                        "FlightID": f.flightID,
                        "Source": f.source,
                        "Destination": f.destination,
                        "Distance": f.distance,
                        "Seats": f.seats,
                        "Active": f.active
                    })
                st.table(rows)
        except Exception as e:
            st.error(f"Error calling listFlights(): {e}")
    else:
        st.info("listFlights() not available. Build non-interactive bindings or run the CLI.")

st.markdown("---")
st.subheader("Booking")

bcol1, bcol2, bcol3 = st.columns(3)

with bcol1:
    st.markdown("### Queue booking")
    if NONINTERACTIVE and hasattr(flight_fms_cpp._fs, "queueBooking"):
        with st.form("queue_booking"):
            bid_fid = st.text_input("Flight ID to queue", value="")
            passenger = st.text_input("Passenger name", value="Alice")
            queued = st.form_submit_button("Queue booking")
            if queued:
                ok = flight_fms_cpp._fs.queueBooking(bid_fid, passenger)
                if ok:
                    st.success(f"Queued booking for {passenger} on {bid_fid}")
                else:
                    st.error("Failed to queue booking — flight not found/active.")
    else:
        st.info("queueBooking not available. Build non-interactive wrappers.")

with bcol2:
    st.markdown("### Process next booking (non-interactive)")
    if NONINTERACTIVE and hasattr(flight_fms_cpp._fs, "processNextBookingNonInteractive"):
        pname = st.text_input("Passenger name to assign when processing", value="AssignedPassenger")
        if st.button("Process next booking"):
            ok, msg = flight_fms_cpp._fs.processNextBookingNonInteractive(pname)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    else:
        st.info("processNextBookingNonInteractive not available. Build bindings.")

with bcol3:
    st.markdown("### Show bookings for a flight")
    fid_q = st.text_input("Flight ID to show bookings", value="")
    if st.button("Show bookings"):
        if NONINTERACTIVE and hasattr(flight_fms_cpp._fs, "getBookingsForFlight"):
            try:
                bookings = flight_fms_cpp._fs.getBookingsForFlight(fid_q)
                if not bookings:
                    st.write("No bookings.")
                else:
                    st.table([{"BookingId": b[0], "Passenger": b[1]} for b in bookings])
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("Non-interactive getBookingsForFlight not available. Build bindings.")

st.markdown("---")
st.subheader("Searches & Graphs")

gcol1, gcol2 = st.columns(2)
with gcol1:
    st.markdown("### Search flights by source")
    src_q = st.text_input("Source", value="")
    if st.button("Search by source"):
        if NONINTERACTIVE and hasattr(flight_fms_cpp._fs, "searchFlightsBySourceNonInteractive"):
            results = flight_fms_cpp._fs.searchFlightsBySourceNonInteractive(src_q)
            if not results:
                st.write("No flights found.")
            else:
                st.table([{"FlightID": f.flightID, "To": f.destination, "Distance": f.distance, "Seats": f.seats} for f in results])
        else:
            st.info("Non-interactive search not available.")

with gcol2:
    st.markdown("### Shortest path (Dijkstra)")
    src = st.text_input("Source airport", value="")
    dst = st.text_input("Destination airport", value="")
    if st.button("Find shortest path"):
        if NONINTERACTIVE and hasattr(flight_fms_cpp._fs, "dijkstraPath"):
            dist, path = flight_fms_cpp._fs.dijkstraPath(src, dst)
            if dist < 0:
                st.error("No path found or error.")
            else:
                st.success(f"Distance = {dist}")
                st.write("Path: " + " -> ".join(path))
        else:
            st.info("Non-interactive dijkstraPath not available. Build bindings.")

st.markdown("---")
st.subheader("Developer / CLI fallback")

st.write("If the non-interactive C++ wrappers are not implemented/built, you can run the native CLI as a fallback (requires `fms_app` executable built in `cpp/`).")
if st.button("Show CLI run instructions"):
    st.code("cd cpp && mkdir build && cd build && cmake .. && make && ../fms_app")

st.write("You can also run `scripts/run_streamlit.sh` locally which sets PYTHONPATH and runs this app.")

st.markdown("----")
st.caption("Streamlit UI — connects to C++ backend via pybind11. Build non-interactive wrappers for full functionality.")