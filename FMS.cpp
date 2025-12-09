#include <iostream>
#include <queue>
#include <stack>
using namespace std;

struct Flight {
    string flightID;
    string source;
    string destination;
    int distance;
    int seats;
};

const int MAX_FLIGHTS = 100;

class FlightSystem {
private:
    Flight flights[MAX_FLIGHTS]; 
    int flightCount = 0;
    stack<string> recentSearches; 
    queue<int> bookingQueue;     

public:
    // adding a new flight
    void addFlight(string id, string src, string dest, int dist, int seats) {
        if (flightCount >= MAX_FLIGHTS) {
            cout << "Cannot add more flights.\n";
            return;
        }
        flights[flightCount] = {id, src, dest, dist, seats};
        flightCount++;
    }

    // displaying all flights
    void displayFlights() {
        for (int i = 0; i < flightCount; i++) {
            cout << flights[i].flightID << ": " << flights[i].source << " -> "
                 << flights[i].destination << ", Distance: " << flights[i].distance
                 << ", Seats: " << flights[i].seats << endl;
        }
    }

    // searching flights from a source
    void searchFlights(string src) {
        cout << "Flights from " << src << ":\n";
        bool found = false;
        for (int i = 0; i < flightCount; i++) {
            if (flights[i].source == src) {
                cout << flights[i].flightID << ": " << flights[i].source << " -> "
                     << flights[i].destination << ", Distance: " << flights[i].distance
                     << ", Seats: " << flights[i].seats << endl;
                recentSearches.push(flights[i].destination);
                found = true;
            }
        }
        if (!found) cout << "No flights found.\n";
    }

    // booking a flight by index
    void bookFlight(int index) {
        if (index < 0 || index >= flightCount) {
            cout << "Invalid flight index!\n";
            return;
        }
        bookingQueue.push(index);
        cout << "Booking request added for flight " << flights[index].flightID << ".\n";
    }

    // processing the next booking
    void processBooking() {
        if (bookingQueue.empty()) {
            cout << "No bookings to process.\n";
            return;
        }
        int index = bookingQueue.front();
        bookingQueue.pop();
        if (flights[index].seats > 0) {
            flights[index].seats--;
            cout << "Booking confirmed for flight " << flights[index].flightID
                 << ". Seats left: " << flights[index].seats << endl;
        } else {
            cout << "No seats available for flight " << flights[index].flightID << endl;
        }
    }
};

int main() {
    FlightSystem system;

    system.addFlight("F101", "Mumbai", "Delhi", 1400, 5);
    system.addFlight("F102", "Delhi", "Bangalore", 2150, 3);
    system.addFlight("F103", "Mumbai", "Bangalore", 980, 2);

    cout << "All Flights:\n";
    system.displayFlights();

    cout << "\nSearch flights from Mumbai:\n";
    system.searchFlights("Mumbai");

    cout << "\nBooking flights:\n";
    system.bookFlight(0);
    system.bookFlight(1); 

    cout << "\nProcessing bookings:\n";
    system.processBooking();
    system.processBooking();
    system.processBooking(); 

    return 0;
}
