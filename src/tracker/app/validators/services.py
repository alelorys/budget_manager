from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MoneyAdd(BaseModel):
    name: Optional[str] = None
    type: Optional[bool] = False
    amount: Optional[float] = None
    category: Optional[str] = None
    
    class Config:
        orm_mode = True
    
class MessageResponse(BaseModel):
    message: str
    
    class Config:
        orm_mode = True
    
class MoneyResponse(BaseModel):
    id: int
    name: str
    type: str
    date: datetime
    amount: float
    category: str
    
    class Config:
        orm_mode = True
        
class MoneyList(BaseModel):
    operations: List[MoneyResponse]
    
class Total(BaseModel):
    total: float
    
    class Config:
        orm_mode = True
        
class FileToPredict(BaseModel):
    path: str