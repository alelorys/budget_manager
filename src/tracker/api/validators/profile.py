from pydantic import BaseModel

class SetPassword(BaseModel):
    new_pwd:str