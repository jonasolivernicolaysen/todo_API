from fastapi import FastAPI
from sqlmodel import SQLModel, Field
import uuid
from uuid import UUID
from datetime import datetime
from enum import Enum

class Status(Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class Todo(SQLModel, table=True):
    id: UUID
    name: str
    created_at: datetime
    due_date: datetime
    status = Status.todo
