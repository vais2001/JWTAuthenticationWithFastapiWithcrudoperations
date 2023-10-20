from fastapi import FastAPI,Depends, HTTPException
from database import Base, engine,get_db
from sqlalchemy.orm import Session
from models import*
import models
from schemas import *
from jwt_handler import signJWT
from jwt_bearer import JWTBearer
from passlib.context import CryptContext



Base.metadata.create_all(engine)

app = FastAPI()



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserSignupSchema):
    hashed_password = password_context.hash(user.password)
    print(hashed_password,111111111111111111)
    db_user = User(email=user.email, password=hashed_password)
    print(db_user,22222222222222)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return signJWT(db_user.email)

@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSignupSchema, db: Session = Depends(get_db)):
    return create_user(db, user)


def check_user(db: Session, data: UserLoginSchema):
    user = db.query(User).filter(User.email == data.email).first()
    if user and password_context.verify(data.password, user.password):
        return user
    return None

@app.post("/user/login", tags=["user"])
def user_login(data: UserLoginSchema, db: Session = Depends(get_db)):
    user = check_user(db, data)
    if user:
        return signJWT(user.email)
    raise HTTPException(status_code=400, detail="Wrong login details")


@app.post("/add_tasks", tags=["tasks"])
def add_post(task: ToDoRequest, user: str = Depends(JWTBearer())):
    db = next(get_db())
    new_task = models.ToDo(task=task.task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added successfully", "status": "success"}



@app.get("/all_tasks/")
def read_todo(user: str = Depends(JWTBearer())):
    db=next(get_db())
    task = db.query(models.ToDo).all()
    print(task)
    return {"todo list": task, "status": "success"}



@app.get("/single_task/{id}")
def read_todo(id,user: str = Depends(JWTBearer())):
    db = next(get_db())
    task = db.query(models.ToDo).filter(models.ToDo.id==id).first()
    if task:
        return {"todo item": task, "status": "success"}
    raise HTTPException(status_code=404, detail="Item not found")



@app.delete("/todo/{id}")
def delete_todo(id,user: str = Depends(JWTBearer())):
    db = next(get_db())
    delete_task=db.query(models.ToDo).filter(models.ToDo.id==id).delete()
    if delete_task:
        db.commit()
        return {"message": f"Deleted successfully with id {id}", "status": "success"} 
    raise HTTPException(status_code=404, detail=f"Item with id {id} not found")



@app.put("/update_todo/{id}")
def updated_todo(id,task:ToDoRequest,user:str=Depends(JWTBearer())):
    db=next(get_db())
    updated_task=db.query(models.ToDo).filter(models.ToDo.id==id)
    if updated_task:
        updated_task.update(task.model_dump())
        db.commit()
        return {"message": f"Updated list with id {id}", "status": "success"}
    raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
