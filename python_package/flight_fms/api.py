from . import _fs, flight_fms_cpp
import subprocess
import os

_fs_instance = _fs

def view_flights():
    _fs_instance.viewFlights()

def show_recent_searches():
    _fs_instance.showRecentSearches()

def run_kruskal_mst():
    _fs_instance.runKruskalMST()

def run_bfs():
    _fs_instance.runBFS()

def run_dfs():
    _fs_instance.runDFS()

def queue_booking_interactive():
    _fs_instance.bookFlight()

def process_next_booking_interactive():
    _fs_instance.processNextBooking()

def cancel_booking_interactive():
    _fs_instance.cancelBooking()

def show_bookings_for_flight_interactive():
    _fs_instance.showBookingsForFlight()

def add_flight_interactive():
    _fs_instance.addFlight()

def cancel_flight_interactive():
    _fs_instance.cancelFlight()

def schedule_flight_interactive():
    _fs_instance.scheduleFlight()

def is_noninteractive_ready():
    return hasattr(flight_fms_cpp, "add_flight_params")

def run_cli_command(cmd_args):
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../cpp/fms_app"))
    if not os.path.exists(exe):
        exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../cpp/fms_app"))
    if not os.path.exists(exe):
        raise FileNotFoundError("Could not find fms_app executable. Build it with CMake first.")
    proc = subprocess.Popen([exe] + cmd_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(timeout=10)
    return out, err, proc.returncode