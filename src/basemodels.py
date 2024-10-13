from pydantic import BaseModel

class InputData(BaseModel):
    """
    A model representing flight input data for processing.

    Attributes:
        tailnumber (str): Unique airplane indentifier.
        A positive value indicates a delayed start,
        while a Negative indicates an early start.
        carrier (str): The airline carrier code.
        origin (str): The code of the origin airport.
        dest (str): The code of the destination airport.
        name (str): Airline name.
        distance (int): The distance of the flight in miles.

    Example:
        input_data = InputData(
            tailnum="N37298",
            carrier="UA",
            origin="EWR",
            dest="RSW",
            name="United Air Lines Inc.",
            distance=1068
        )
    """
    tailnum: str
    carrier: str
    origin: str
    dest: str
    name: str
    distance: int
