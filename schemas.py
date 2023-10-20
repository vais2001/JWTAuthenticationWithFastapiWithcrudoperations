
from pydantic import BaseModel, EmailStr
class ToDoRequest(BaseModel):
    id:int
    task: str

class UserSignupSchema(BaseModel):
    fullname: str 
    email: EmailStr 
    password: str 
    
    
class UserLoginSchema(BaseModel):
    email: EmailStr 
    password: str