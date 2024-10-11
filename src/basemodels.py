from pydantic import BaseModel

class InputData(BaseModel):
    dep_delay: float
    carrier: str
    origin: str
    dest: str
    air_time: float
    distance: int