from pydantic import BaseModel

class AddCategory(BaseModel):
    name: str

class CategoryList(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class DeleteCategory(BaseModel):
    id: int