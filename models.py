from database import Base
from sqlalchemy import Column, Integer, String
class ToDo(Base):
    __tablename__ = 'todo_list'
    id = Column(Integer, primary_key=True)
    task =  Column(String(50))
    
class User(Base):
    __tablename__= 'users'
    id = Column(Integer,primary_key=True,index=True)
    email= Column(String,unique=True)
    password=Column(String)
    