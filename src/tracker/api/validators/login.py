from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    
class User(BaseModel):
    id: int
    username: str
    name: str
    lastname: str

class UserInDB(User):
    password: str

class AddUser(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    