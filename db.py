from flask_sqlalchemy import SQLAlchemy
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum

db = SQLAlchemy()

class Status(Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(200))
    created_at = db.Column(db.String(40))
    due_date = db.Column(db.String(40))
    status = db.Column(db.String(40))

