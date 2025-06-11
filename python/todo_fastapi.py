from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from typing import Optional
import os

# Set your DATABASE_URL or read from environment
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:yourpassword@localhost:5432/yourdb")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:k0sWi6tGuLOV@noisy-thunder-80402718.us-west-2.aws.neon.tech/v2-simple-to-do-gm_db_8492381?options=project%3Dnoisy-thunder-80402718&sslmode=require")

engine = create_engine(
    DATABASE_URL,
    pool_size=5,         # avoid high values in serverless environments
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Todo API", version="1.0")

# --- SQLAlchemy Models ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    is_online = Column(Boolean, default=False)
    country = Column(String(255))

    todos = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="todos")


# --- Pydantic Schemas ---
from pydantic import BaseModel
from typing import Optional, List


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: int


class TodoRead(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_online:  Optional[bool] = True
    country: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    country: Optional[str] = None
    is_online: Optional[bool] = None


class UserRead(BaseModel):
    id: int
    name:  Optional[str] = None
    email: Optional[str] = None
    is_online:  Optional[bool] = True
    country: Optional[str] = None

    class Config:
        orm_mode = True


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- CRUD Endpoints ---

## USERS
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@app.get("/users/", response_model=List[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}/todos", response_model=List[TodoRead])
def get_todos_by_user(user_id: int, db: Session = Depends(get_db)):
    todos = db.query(Todo).filter(Todo.user_id == user_id).all()
    return todos

## TODOS
@app.post("/todos/", response_model=TodoRead)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoRead])
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, updated: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated.dict().items():
        setattr(todo, key, value)
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted"}
