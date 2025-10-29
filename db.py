from flask_sqlalchemy import SQLAlchemy
from uuid import UUID, uuid4
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.String(40), nullable=False)
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

