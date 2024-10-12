from pydantic import BaseModel

class InputData(BaseModel):
    """
    A model representing flight input data for processing.

    Attributes:
        dep_delay (float): The delay of the departure in minutes.
        A positive value indicates a delayed start,
        while a Negative indicates an early start.
        carrier (str): The airline carrier code.
        origin (str): The code of the origin airport.
        dest (str): The code of the destination airport.
        air_time (float): The duration of the flight in minutes.
        distance (int): The distance of the flight in miles.

    Example:
        input_data = InputData(
            dep_delay=15.0,
            carrier='AA',
            origin='JFK',
            dest='LAX',
            air_time=300.0,
            distance=2475
        )
    """
    dep_delay: float
    carrier: str
    origin: str
    dest: str
    air_time: float
    distance: int
