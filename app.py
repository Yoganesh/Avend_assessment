from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import uvicorn

engine = create_engine("mysql://avend:secret@172.17.0.1:3306/avend_db")


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(20), unique=True, index=True)
    hashedPassword = Column(String(30))
    name = Column(String(20))
    age = Column(Integer)


Base.metadata.create_all(engine)


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int


class UpdateUser(BaseModel):
    name: str
    age: int


app = FastAPI()


@app.post("/create_user")
def create_user(data: CreateUser):
    session = Session(bind=engine, expire_on_commit=False)
    try:
        userdb = User(email=data.email.lower(), hashedPassword=data.password + "notreallyhashed", name=data.name,
                      age=data.age)
        session.add(userdb)
        session.commit()
        session.close()
        return JSONResponse(status_code=201, content={"result": True, "message": "User created successfully"})
    except IntegrityError:
        return JSONResponse(status_code=200, content={"result": False, "message": "User already exists"})


@app.get("/get_user/{user_id}")
def get_user(user_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    user = session.query(User).get(user_id)
    print(type(user))
    if user:
        return JSONResponse(status_code=200, content={"result": True, "data": dict(name=user.name, age=user.age)})
    else:
        return JSONResponse(status_code=404, content={"result": True, "message": f"user with id {user_id} not found"})


@app.put("/update_user/{user_id}")
def update_user(user_id: int, data: UpdateUser):
    session = Session(bind=engine, expire_on_commit=False)
    user = session.query(User).get(user_id)
    if user:
        user.name = data.name
        user.age = data.age
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content={"result": True, "message": f"User with id {user_id} details updated"})
    else:
        session.close()
        return JSONResponse(status_code=404, content={"result": True, "message": f"user with id {user_id} not found"})


@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    session = Session(bind=engine, expire_on_commit=False)

    user = session.query(User).get(user_id)

    if user:
        fstring = f"user with id {user.id} deleted"
        session.delete(user)
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content={"result": True, "data": fstring})
    else:
        session.close()
        return JSONResponse(status_code=404, content={"result": True, "message": f"user with id {user_id} not found"})


@app.get("/getAllUsers")
def getAllUsers():

    session = Session(bind=engine, expire_on_commit=False)

    user_list = session.query(User).all()

    # close the session
    session.close()

    return user_list


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=6655)
