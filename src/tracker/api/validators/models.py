from pydantic import BaseModel
from typing import List, Any
from datetime import datetime

class DeleteModel(BaseModel):
    id: int

class ActivateModel(BaseModel):
    id: int


class ModelInfo(BaseModel):
    model_name: str
    date: datetime
    status: bool

    class Config:
        orm_mode = True

class ModelList(BaseModel):
    model_list: List[ModelInfo] = None

    class Config:
        orm_mode = True