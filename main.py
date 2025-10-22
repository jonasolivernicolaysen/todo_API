from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from .db import Status, Todo, engine
from datetime import datetime, timezone

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/todos")
def add_todo(name: str, due_date: datetime, status: Status):
    with Session(engine) as session:
        todo = Todo(
            name=name,
            due_date=due_date,
            status=status
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        print(todo)


@app.get("/todos")
def list_todos(session: Session = Depends(get_session)):
    with Session(engine) as session:
        # get all todos
        return session.exec(select(Todo)).all()
    

@app.get("/")
def root():
    return {"status": "ok", "service": "todo-api"}