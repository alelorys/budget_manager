from pydantic import BaseModel

class Predict(BaseModel):
    predicted: float

    class Config:
        orm_mode = True