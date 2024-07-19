from pydantic import BaseModel
from datetime import datetime
class Predict(BaseModel):
    predicted: float
    real: float
    date: datetime
    user_id: int

    class Config:
        orm_mode = True