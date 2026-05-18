from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    
class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str