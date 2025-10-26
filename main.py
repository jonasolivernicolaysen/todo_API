from flask import Flask, render_template, redirect, url_for, request, session
from db import Status, Todo, db
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import and_, func

# app setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

# initialize sqlalchemy
db.init_app(app)

# create new database every start, this is only for testing purposes
with app.app_context():
    db.drop_all()
    db.create_all()

# routes
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/create_todo", methods=["GET", "POST"])
def create_todo():
    session.clear()

    name = request.form.get("form_name") 
    description = request.form.get("form_description")
    due_date = request.form.get("form_due_date")
    created_at = datetime.now().strftime("%I:%M:%S %p").lstrip("0")

    if not name:
        return render_template("create_todo.html", error="Name is required")
        
    new_todo = Todo()
    new_todo.name = name
    new_todo.description = description or ""
    new_todo.created_at = created_at
    new_todo.due_date = due_date or ""
    new_todo.status = "todo"
    
    db.session.add(new_todo)
    db.session.commit()

    return render_template("create_todo.html")

@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return {"todos": [t.to_dict() for t in todos]}