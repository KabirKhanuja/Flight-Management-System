## Flight Management System – C++ (DSA Project)

This is a console‑based Flight Management System implemented in C++ to demonstrate core Data Structures and Algorithms in a single, simple application.

### Features

- **Admin**
	- Add flight (ID, source, destination, distance, seats)
	- Cancel flight (mark as inactive)
	- Schedule/activate flight (reactivate a cancelled flight)
- **User**
	- View all active flights
	- Book a flight (queued booking, confirmed when processed)
	- Process next booking (assign seat + booking ID)
	- Cancel booking by Booking ID
	- Show bookings for a flight
	- Search flights by source
	- Show recent search history (stack)
- **Graph / Algorithms**
	- Shortest distance between two airports (Dijkstra)
	- DFS & BFS traversals on airport graph
	- Prim’s MST and Kruskal’s MST over airport network

### Data Structures Used

- **Array**: `Flight flights[MAX_FLIGHTS]` – stores all flight records.
- **Linked List**: `BookingNode` per flight – booking list for each flight.
- **Stack**: `stack<string> recentSearches` – recent search sources.
- **Queue**: `queue<int> bookingQueue` – pending bookings (FIFO).
- **Binary Search Tree (BST)**: `FlightBST` – index on `flightID` for fast lookup and in‑order display.
- **Graph (Adjacency List)**: `AirportGraph` – airports as nodes, flights as weighted edges.
- **Hashing**: `unordered_map<string,int> airportIndex` – airport name → graph index.
- **Disjoint Set Union (DSU)**: used inside `AirportGraph::kruskalMST()`.

### Algorithms Used

- **DFS**: depth‑first traversal from a given airport.
- **BFS**: breadth‑first traversal from a given airport.
- **Dijkstra**: shortest path (minimum total distance) between two airports.
- **Prim’s Algorithm**: minimum spanning tree starting from a chosen airport.
- **Kruskal’s Algorithm**: minimum spanning tree using sorted edges + DSU.

### Relevant Files

- `FMS.cpp` – main C++ implementation and `main()` with menu.
- `fms.h` – header with declarations for the main data structures and classes.

### Build and Run

From the `cpp` folder:

```bash
cd cpp
g++ FMS.cpp -o FMS -std=c++17
./FMS
```

### Basic Usage (Menu)

When you run `./FMS`, you’ll see a menu:

- `1` – Admin: Add Flight  
- `2` – Admin: Cancel Flight  
- `3` – Admin: Schedule/Activate Flight  
- `4` – User: View Flights  
- `5` – User: Book Flight (queue)  
- `6` – User: Process Next Booking  
- `7` – User: Cancel Booking  
- `8` – User: Show Bookings For Flight  
- `9` – Search Flights by Source  
- `10` – Show Recent Search Stack  
- `11` – Shortest Distance Between Airports (Dijkstra)  
- `12` – DFS on Airport Graph  
- `13` – BFS on Airport Graph  
- `14` – Prim’s MST on Airport Graph  
- `15` – Kruskal’s MST on Airport Graph  
- `0` – Exit

Add a few flights first so the graph‑based algorithms (Dijkstra/DFS/BFS/Prim/Kruskal) have airports and connections to work on.

