#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../cpp/fms.h"

namespace py = pybind11;

PYBIND11_MODULE(flight_fms_cpp, m) {
    m.doc() = "pybind11 bindings for Flight Management System (FMS)";

    py::class_<BookingNode>(m, "BookingNode")
        .def(py::init<int, const std::string&>(),
             py::arg("bookingId") = 0, py::arg("passengerName") = std::string(""))
        .def_readwrite("bookingId", &BookingNode::bookingId)
        .def_readwrite("passengerName", &BookingNode::passengerName)
        .def_readwrite("next", &BookingNode::next);

    py::class_<Flight>(m, "Flight")
        .def(py::init<>())
        .def_readwrite("flightID", &Flight::flightID)
        .def_readwrite("source", &Flight::source)
        .def_readwrite("destination", &Flight::destination)
        .def_readwrite("distance", &Flight::distance)
        .def_readwrite("seats", &Flight::seats)
        .def_readwrite("active", &Flight::active)
        .def_readonly("bookingHead", &Flight::bookingHead)
        .def("__repr__", [](const Flight &f){
            return "<Flight id='" + f.flightID + "' " + f.source + "->" + f.destination + " seats=" + std::to_string(f.seats) + ">";
        });

    py::class_<FlightBSTNode>(m, "FlightBSTNode")
        .def(py::init<Flight*>(),
             py::arg("flightPtr") = nullptr)
        .def_readwrite("flightPtr", &FlightBSTNode::flightPtr)
        .def_readwrite("left", &FlightBSTNode::left)
        .def_readwrite("right", &FlightBSTNode::right);

    py::class_<FlightBST>(m, "FlightBST")
        .def(py::init<>())
        .def("insert", &FlightBST::insert, "Insert a Flight* into BST")
        .def("search", &FlightBST::search, "Search a flight by id and return Flight*")
        .def("displayInOrder", &FlightBST::displayInOrder, "Print flights in-order (to stdout)");

    py::class_<AirportGraph>(m, "AirportGraph")
        .def(py::init<>())
        .def("getAirportIndex", &AirportGraph::getAirportIndex, "Get or create index for airport", py::arg("name"))
        .def("addEdge", &AirportGraph::addEdge, "Add undirected edge between airports", py::arg("src"), py::arg("dest"), py::arg("dist"))
        .def("DFS", &AirportGraph::DFS, "Depth-first traversal from start airport", py::arg("start"))
        .def("BFS", &AirportGraph::BFS, "Breadth-first traversal from start airport", py::arg("start"))
        .def("dijkstra", &AirportGraph::dijkstra, "Compute shortest path (Dijkstra) between source and dest", py::arg("source"), py::arg("dest"))
        .def("primMST", &AirportGraph::primMST, "Run Prim's MST starting from given airport", py::arg("start"))
        .def("kruskalMST", &AirportGraph::kruskalMST, "Run Kruskal's MST on the graph");

    py::class_<FlightSystem>(m, "FlightSystem")
        .def(py::init<>())
        .def("addFlight", &FlightSystem::addFlight, "Interactive: add flight (reads from stdin)")
        .def("cancelFlight", &FlightSystem::cancelFlight, "Interactive: cancel flight (reads from stdin)")
        .def("scheduleFlight", &FlightSystem::scheduleFlight, "Interactive: schedule/activate flight (reads from stdin)")
        .def("viewFlights", &FlightSystem::viewFlights, "Print active flights (in-order via BST)")

        .def("bookFlight", &FlightSystem::bookFlight, "Interactive: queue a booking request (reads from stdin)")
        .def("processNextBooking", &FlightSystem::processNextBooking, "Interactive: process next queued booking (reads passenger name from stdin)")
        .def("cancelBooking", &FlightSystem::cancelBooking, "Interactive: cancel booking (reads from stdin)")
        .def("showBookingsForFlight", &FlightSystem::showBookingsForFlight, "Interactive: show bookings for a flight (reads flight id from stdin)")

        .def("searchFlightsBySource", &FlightSystem::searchFlightsBySource, "Interactive: search flights by source (reads source from stdin)")
        .def("showRecentSearches", &FlightSystem::showRecentSearches, "Print recent search stack")

        .def("shortestDistanceBetweenAirports", &FlightSystem::shortestDistanceBetweenAirports, "Interactive: Dijkstra (reads source/dest from stdin)")
        .def("runDFS", &FlightSystem::runDFS, "Interactive: DFS (reads start from stdin)")
        .def("runBFS", &FlightSystem::runBFS, "Interactive: BFS (reads start from stdin)")
        .def("runPrimMST", &FlightSystem::runPrimMST, "Interactive: Prim's MST (reads start from stdin)")
        .def("runKruskalMST", &FlightSystem::runKruskalMST, "Run Kruskal's MST (non-interactive)");

    m.attr("__doc__") = "Bindings expose core FMS types; many methods are still interactive and use stdin/stdout. "
                        "If you want non-interactive wrappers (recommended for Streamlit), ask me to add parameterized wrapper methods next.";
}