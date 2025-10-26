from flask_sqlalchemy import SQLAlchemy
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum

db = SQLAlchemy()

class Status(Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"<User id: {self.id}, Name: {self.username}"


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(200))
    created_at = db.Column(db.String(40))
    due_date = db.Column(db.String(40))
    status = db.Column(db.String(40))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "due_date": self.due_date,
            "status": self.status,
        }

    def __repr__(self) -> str:
        return f"<Todo: {self.id, self.name, self.description, self.created_at, self.due_date, self.status}>"
