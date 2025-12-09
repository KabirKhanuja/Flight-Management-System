#pragma once

#include <string>
#include <vector>
#include <stack>
#include <queue>
#include <unordered_map>

struct BookingNode {
    int bookingId;
    std::string passengerName;
    BookingNode* next;
    BookingNode(int id = 0, const std::string& name = "");
};

struct Flight {
    std::string flightID;
    std::string source;
    std::string destination;
    int distance;
    int seats;
    bool active;
    BookingNode* bookingHead;
    Flight();
};

const int MAX_FLIGHTS = 100;

struct FlightBSTNode {
    Flight* flightPtr;
    FlightBSTNode* left;
    FlightBSTNode* right;
    FlightBSTNode(Flight* f = nullptr);
};

class FlightBST {
private:
    FlightBSTNode* root;
    FlightBSTNode* insertRec(FlightBSTNode* node, Flight* f);
    void inorderRec(FlightBSTNode* node);
    Flight* searchRec(FlightBSTNode* node, const std::string& id);
public:
    FlightBST();
    ~FlightBST();
    void insert(Flight* f);
    Flight* search(const std::string& id);
    void displayInOrder();
};

class AirportGraph {
public:
    AirportGraph();
    int getAirportIndex(const std::string& name);
    void addEdge(const std::string& src, const std::string& dest, int dist);
    void DFS(const std::string& start);
    void BFS(const std::string& start);
    void dijkstra(const std::string& source, const std::string& dest);
    void primMST(const std::string& start);
    void kruskalMST();

private:
    struct Edge { int u, v, w; };
    struct DSU {
        std::vector<int> parent, rnk;
        DSU(int n = 0);
        void init(int n);
        int find(int x);
        bool unite(int a, int b);
    };

    std::unordered_map<std::string,int> airportIndex;
    std::vector<std::string> indexToAirport;
    std::vector<std::vector<std::pair<int,int>>> adj;

    void dfsUtil(int u, std::vector<bool>& visited);
};

class FlightSystem {
public:
    FlightSystem();
    // admin
    void addFlight();
    void cancelFlight();
    void scheduleFlight();
    void viewFlights();

    // booking flow
    void bookFlight();
    void processNextBooking();
    void cancelBooking();
    void showBookingsForFlight();

    // searches / stack
    void searchFlightsBySource();
    void showRecentSearches();

    // graph algorithms
    void shortestDistanceBetweenAirports();
    void runDFS();
    void runBFS();
    void runPrimMST();
    void runKruskalMST();

private:
    Flight flights[MAX_FLIGHTS];
    int flightCount;
    FlightBST bst;
    std::stack<std::string> recentSearches;
    std::queue<int> bookingQueue;
    AirportGraph graph;
    int globalBookingId;
};