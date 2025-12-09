try:
    import flight_fms_cpp 
except Exception as e:
    raise ImportError(
        "Could not import compiled extension 'flight_fms_cpp'. "
        "Did you run `scripts/build_extension.sh`? Original error: " + str(e)
    )

_fs = flight_fms_cpp.FlightSystem()

Flight = flight_fms_cpp.Flight
BookingNode = flight_fms_cpp.BookingNode
AirportGraph = flight_fms_cpp.AirportGraph
FlightSystem = flight_fms_cpp.FlightSystem

__all__ = [
    "flight_fms_cpp",
    "Flight",
    "BookingNode",
    "AirportGraph",
    "FlightSystem",
    "_fs",
]