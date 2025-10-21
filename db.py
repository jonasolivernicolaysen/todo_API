from fastapi import FastAPI
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum

class Status(Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False, max_length=30) 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    due_date: datetime | None = None
    status: Status = Field(default=Status.todo)


