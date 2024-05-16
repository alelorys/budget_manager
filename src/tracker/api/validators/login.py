from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: str
    
class User(BaseModel):
    id: int
    login: str
    name: str
    lastname: str

class UserInDB(User):
    password: str

class AddUser(BaseModel):
    login: str
    name: str
    lastname: str
    password: str
    