from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from db import Status, Todo, User, db
from datetime import datetime
from typing import Optional
from sqlalchemy import and_, func
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


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
# i need to retrieve all the todos from the db, then pass all of them through a js function to visualize in the div
@app.route("/", methods=["GET", "POST"])
def home():
    todos = Todo.query.all()
    jsonified_todos = [todo.to_dict() for todo in todos]
    return render_template("home.html", todos=jsonified_todos)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":   
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    password_check = request.form.get("password_check")
    
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("register.html", error="Username already taken")

    if password != password_check:
        return render_template("register.html", error="Passwords must match")
    
    new_user = User()
    new_user.username = username
    new_user.password = password
    
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    # check if user is in the db, if not give an error
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return redirect(url_for("home"))
    else:
        return render_template("login.html", error="User not found")


@app.route("/create_todo", methods=["GET", "POST"])
def create_todo():
    if request.method == "GET":
        return render_template("create_todo.html")

    name = request.form.get("form_name") 
    description = request.form.get("form_description")
    due_date = request.form.get("form_due_date")
    created_at = datetime.now().strftime("%Y-%m-%d")

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

    return redirect(url_for("home"))


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return {"todos": [t.to_dict() for t in todos]}


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return {"todos": [t.to_dict() for t in users]}