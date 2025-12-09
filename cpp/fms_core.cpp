#include "fms.h"
#include <iostream>
#include <algorithm>
#include <climits>

using namespace std;

BookingNode::BookingNode(int id, const std::string& name)
    : bookingId(id), passengerName(name), next(nullptr) {}

Flight::Flight()
    : flightID(), source(), destination(), distance(0), seats(0), active(true), bookingHead(nullptr) {}

FlightBSTNode::FlightBSTNode(Flight* f)
    : flightPtr(f), left(nullptr), right(nullptr) {}

FlightBST::FlightBST() : root(nullptr) {}

FlightBST::~FlightBST() {
    vector<FlightBSTNode*> stackNodes;
    if (root) stackNodes.push_back(root);
    while (!stackNodes.empty()) {
        FlightBSTNode* node = stackNodes.back();
        stackNodes.pop_back();
        if (node->left) stackNodes.push_back(node->left);
        if (node->right) stackNodes.push_back(node->right);
        delete node;
    }
}

FlightBSTNode* FlightBST::insertRec(FlightBSTNode* node, Flight* f) {
    if (!node) return new FlightBSTNode(f);
    if (f->flightID < node->flightPtr->flightID) {
        node->left = insertRec(node->left, f);
    } else if (f->flightID > node->flightPtr->flightID) {
        node->right = insertRec(node->right, f);
    }
    return node;
}

void FlightBST::inorderRec(FlightBSTNode* node) {
    if (!node) return;
    inorderRec(node->left);
    Flight* f = node->flightPtr;
    if (f->active) {
        cout << f->flightID << ": " << f->source << " -> "
             << f->destination << ", Dist: " << f->distance
             << ", Seats: " << f->seats << '\n';
    }
    inorderRec(node->right);
}

Flight* FlightBST::searchRec(FlightBSTNode* node, const std::string& id) {
    if (!node) return nullptr;
    if (id == node->flightPtr->flightID) return node->flightPtr;
    if (id < node->flightPtr->flightID) return searchRec(node->left, id);
    return searchRec(node->right, id);
}

void FlightBST::insert(Flight* f) {
    root = insertRec(root, f);
}

Flight* FlightBST::search(const std::string& id) {
    return searchRec(root, id);
}

void FlightBST::displayInOrder() {
    inorderRec(root);
}

AirportGraph::AirportGraph() {}

int AirportGraph::getAirportIndex(const std::string& name) {
    auto it = airportIndex.find(name);
    if (it != airportIndex.end()) return it->second;
    int idx = static_cast<int>(indexToAirport.size());
    airportIndex[name] = idx;
    indexToAirport.push_back(name);
    adj.push_back({});
    return idx;
}

void AirportGraph::addEdge(const std::string& src, const std::string& dest, int dist) {
    int u = getAirportIndex(src);
    int v = getAirportIndex(dest);
    adj[u].push_back({v, dist});
    adj[v].push_back({u, dist});
}

void AirportGraph::dfsUtil(int u, std::vector<bool>& visited) {
    visited[u] = true;
    cout << indexToAirport[u] << " ";
    for (auto &p : adj[u]) {
        int v = p.first;
        if (!visited[v]) dfsUtil(v, visited);
    }
}

void AirportGraph::DFS(const std::string& start) {
    if (!airportIndex.count(start)) {
        cout << "Airport not found.\n";
        return;
    }
    vector<bool> visited(adj.size(), false);
    cout << "DFS from " << start << ": ";
    dfsUtil(airportIndex[start], visited);
    cout << '\n';
}

void AirportGraph::BFS(const std::string& start) {
    if (!airportIndex.count(start)) {
        cout << "Airport not found.\n";
        return;
    }
    vector<bool> visited(adj.size(), false);
    queue<int> q;
    int s = airportIndex[start];
    visited[s] = true;
    q.push(s);
    cout << "BFS from " << start << ": ";
    while (!q.empty()) {
        int u = q.front(); q.pop();
        cout << indexToAirport[u] << " ";
        for (auto &p : adj[u]) {
            int v = p.first;
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
    cout << '\n';
}

void AirportGraph::dijkstra(const std::string& source, const std::string& dest) {
    if (!airportIndex.count(source) || !airportIndex.count(dest)) {
        cout << "Source or destination airport not found.\n";
        return;
    }
    int n = static_cast<int>(adj.size());
    vector<int> dist(n, INT_MAX);
    vector<int> parent(n, -1);
    using PII = pair<int,int>;
    priority_queue<PII, vector<PII>, greater<PII>> pq;

    int s = airportIndex[source];
    int t = airportIndex[dest];
    dist[s] = 0;
    pq.push({0, s});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto &p : adj[u]) {
            int v = p.first, w = p.second;
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }

    if (dist[t] == INT_MAX) {
        cout << "No path found between " << source << " and " << dest << ".\n";
        return;
    }

    cout << "Shortest distance from " << source << " to " << dest << " = " << dist[t] << "\n";
    vector<int> path;
    for (int cur = t; cur != -1; cur = parent[cur]) path.push_back(cur);
    reverse(path.begin(), path.end());
    cout << "Path: ";
    for (size_t i = 0; i < path.size(); ++i) {
        cout << indexToAirport[path[i]];
        if (i + 1 < path.size()) cout << " -> ";
    }
    cout << "\n";
}

std::pair<int, std::vector<std::string>> AirportGraph::dijkstra_path(const std::string& source, const std::string& dest) {
    if (!airportIndex.count(source) || !airportIndex.count(dest)) {
        return {INT_MAX, {}};
    }
    int n = static_cast<int>(adj.size());
    vector<int> dist(n, INT_MAX);
    vector<int> parent(n, -1);
    using PII = pair<int,int>;
    priority_queue<PII, vector<PII>, greater<PII>> pq;

    int s = airportIndex[source];
    int t = airportIndex[dest];
    dist[s] = 0;
    pq.push({0, s});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto &p : adj[u]) {
            int v = p.first, w = p.second;
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }

    if (dist[t] == INT_MAX) {
        return {INT_MAX, {}};
    }

    vector<int> pathIdx;
    for (int cur = t; cur != -1; cur = parent[cur]) pathIdx.push_back(cur);
    reverse(pathIdx.begin(), pathIdx.end());
    vector<string> pathNames;
    for (int idx : pathIdx) pathNames.push_back(indexToAirport[idx]);
    return {dist[t], pathNames};
}

void AirportGraph::primMST(const std::string& start) {
    if (!airportIndex.count(start)) {
        cout << "Airport not found.\n";
        return;
    }
    int n = static_cast<int>(adj.size());
    vector<int> key(n, INT_MAX);
    vector<int> parent(n, -1);
    vector<bool> inMST(n, false);
    using PII = pair<int,int>;
    priority_queue<PII, vector<PII>, greater<PII>> pq;

    int s = airportIndex[start];
    key[s] = 0;
    pq.push({0, s});

    while (!pq.empty()) {
        int u = pq.top().second; pq.pop();
        if (inMST[u]) continue;
        inMST[u] = true;
        for (auto &p : adj[u]) {
            int v = p.first, w = p.second;
            if (!inMST[v] && w < key[v]) {
                key[v] = w;
                parent[v] = u;
                pq.push({key[v], v});
            }
        }
    }

    cout << "Prim's MST edges:\n";
    int total = 0;
    for (int v = 0; v < n; ++v) {
        if (parent[v] != -1) {
            cout << indexToAirport[parent[v]] << " - " << indexToAirport[v]
                 << " (" << key[v] << ")\n";
            total += key[v];
        }
    }
    cout << "Total MST weight = " << total << "\n";
}

AirportGraph::DSU::DSU(int n) {
    init(n);
}

void AirportGraph::DSU::init(int n) {
    parent.resize(n);
    rnk.assign(n, 0);
    for (int i = 0; i < n; ++i) parent[i] = i;
}

int AirportGraph::DSU::find(int x) {
    if (parent[x] == x) return x;
    return parent[x] = find(parent[x]);
}

bool AirportGraph::DSU::unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return false;
    if (rnk[a] < rnk[b]) swap(a, b);
    parent[b] = a;
    if (rnk[a] == rnk[b]) rnk[a]++;
    return true;
}

void AirportGraph::kruskalMST() {
    int n = static_cast<int>(adj.size());
    vector<Edge> edges;
    for (int u = 0; u < n; ++u) {
        for (auto &p : adj[u]) {
            int v = p.first, w = p.second;
            if (u < v) edges.push_back({u, v, w});
        }
    }
    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.w < b.w;
    });

    DSU dsu(n);
    int total = 0;
    cout << "Kruskal's MST edges:\n";
    for (auto &e : edges) {
        if (dsu.unite(e.u, e.v)) {
            cout << indexToAirport[e.u] << " - " << indexToAirport[e.v]
                 << " (" << e.w << ")\n";
            total += e.w;
        }
    }
    cout << "Total MST weight = " << total << "\n";
}

FlightSystem::FlightSystem()
    : flightCount(0), bst(), recentSearches(), bookingQueue(), graph(), globalBookingId(1) {}

void FlightSystem::addFlight() {
    if (flightCount >= MAX_FLIGHTS) {
        cout << "Cannot add more flights.\n";
        return;
    }
    Flight &f = flights[flightCount];
    cout << "Enter Flight ID: ";
    cin >> f.flightID;
    cout << "Enter Source: ";
    cin >> f.source;
    cout << "Enter Destination: ";
    cin >> f.destination;
    cout << "Enter Distance: ";
    cin >> f.distance;
    cout << "Enter Seats: ";
    cin >> f.seats;
    f.active = true;
    f.bookingHead = nullptr;
    bst.insert(&f);
    graph.addEdge(f.source, f.destination, f.distance);
    cout << "Flight added at index " << flightCount << ".\n";
    flightCount++;
}

void FlightSystem::cancelFlight() {
    string id;
    cout << "Enter Flight ID to cancel: ";
    cin >> id;
    Flight* f = bst.search(id);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }
    f->active = false;
    cout << "Flight " << id << " marked as cancelled.\n";
}

void FlightSystem::scheduleFlight() {
    string id;
    cout << "Enter Flight ID to schedule/activate: ";
    cin >> id;
    Flight* f = bst.search(id);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }
    f->active = true;
    cout << "Flight " << id << " marked as active/scheduled.\n";
}

void FlightSystem::viewFlights() {
    cout << "Active flights (in-order by ID from BST):\n";
    bst.displayInOrder();
}

void FlightSystem::bookFlight() {
    string id, name;
    cout << "Enter Flight ID to book: ";
    cin >> id;
    Flight* f = bst.search(id);
    if (!f || !f->active) {
        cout << "Flight not found or not active.\n";
        return;
    }
    cout << "Enter passenger name: ";
    cin >> name;
    int index = -1;
    for (int i = 0; i < flightCount; ++i) {
        if (flights[i].flightID == id) {
            index = i; break;
        }
    }
    if (index == -1) {
        cout << "Internal error: index not found.\n";
        return;
    }
    bookingQueue.push(index);
    cout << "Booking request queued for " << id << ".\n";
}

void FlightSystem::processNextBooking() {
    if (bookingQueue.empty()) {
        cout << "No bookings to process.\n";
        return;
    }
    int index = bookingQueue.front(); bookingQueue.pop();
    Flight &f = flights[index];
    if (!f.active) {
        cout << "Flight " << f.flightID << " is cancelled. Cannot process booking.\n";
        return;
    }
    if (f.seats <= 0) {
        cout << "No seats left on flight " << f.flightID << ".\n";
        return;
    }
    string name;
    cout << "Processing booking for flight " << f.flightID << ". Enter passenger name: ";
    cin >> name;
    f.seats--;
    BookingNode* node = new BookingNode(globalBookingId++, name);
    node->next = f.bookingHead;
    f.bookingHead = node;
    cout << "Booking confirmed for " << name << " on " << f.flightID
         << ". Seats left: " << f.seats << "\n";
}

void FlightSystem::cancelBooking() {
    string id;
    int bid;
    cout << "Enter Flight ID: ";
    cin >> id;
    cout << "Enter Booking ID to cancel: ";
    cin >> bid;
    Flight* f = bst.search(id);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }
    BookingNode* cur = f->bookingHead;
    BookingNode* prev = nullptr;
    while (cur && cur->bookingId != bid) {
        prev = cur;
        cur = cur->next;
    }
    if (!cur) {
        cout << "Booking ID not found.\n";
        return;
    }
    if (prev) prev->next = cur->next;
    else f->bookingHead = cur->next;
    delete cur;
    f->seats++;
    cout << "Booking cancelled and seat restored on flight " << id << ".\n";
}

void FlightSystem::showBookingsForFlight() {
    string id;
    cout << "Enter Flight ID: ";
    cin >> id;
    Flight* f = bst.search(id);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }
    cout << "Bookings for flight " << id << ":\n";
    BookingNode* cur = f->bookingHead;
    if (!cur) {
        cout << "No bookings.\n";
        return;
    }
    while (cur) {
        cout << "BookingID: " << cur->bookingId
             << ", Name: " << cur->passengerName << "\n";
        cur = cur->next;
    }
}

void FlightSystem::searchFlightsBySource() {
    string src;
    cout << "Enter source: ";
    cin >> src;
    bool found = false;
    for (int i = 0; i < flightCount; ++i) {
        Flight &f = flights[i];
        if (f.source == src && f.active) {
            cout << f.flightID << ": " << f.source << " -> " << f.destination
                 << ", Dist: " << f.distance << ", Seats: " << f.seats << "\n";
            recentSearches.push(src);
            found = true;
        }
    }
    if (!found) cout << "No active flights from this source.\n";
}

void FlightSystem::showRecentSearches() {
    cout << "Recent search sources (stack top to bottom): ";
    stack<string> temp = recentSearches;
    while (!temp.empty()) {
        cout << temp.top() << " ";
        temp.pop();
    }
    cout << "\n";
}

void FlightSystem::shortestDistanceBetweenAirports() {
    string a, b;
    cout << "Enter source airport: ";
    cin >> a;
    cout << "Enter destination airport: ";
    cin >> b;
    graph.dijkstra(a, b);
}

void FlightSystem::runDFS() {
    string a;
    cout << "Enter start airport for DFS: ";
    cin >> a;
    graph.DFS(a);
}

void FlightSystem::runBFS() {
    string a;
    cout << "Enter start airport for BFS: ";
    cin >> a;
    graph.BFS(a);
}

void FlightSystem::runPrimMST() {
    string a;
    cout << "Enter start airport for Prim's MST: ";
    cin >> a;
    graph.primMST(a);
}

void FlightSystem::runKruskalMST() {
    graph.kruskalMST();
}
