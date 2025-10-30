from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response
from db import Todo, User, db
from datetime import datetime
from typing import Optional
from sqlalchemy import and_, func
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_access_cookies


# app setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["JWT_SECRET_KEY"] = "jwtsecretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

# initialize jwt authentication
jwt = JWTManager(app)

# initialize sqlalchemy
db.init_app(app)

# create new database every start, this is only for testing purposes
""" with app.app_context():
    db.drop_all()
    db.create_all()
 """
# routes
@app.route("/", methods=["GET", "POST"])
def authenticate():
    return render_template("authenticate.html")


@app.route("/home", methods=["GET", "POST"])
@jwt_required()
def home():
    username = session.get("username")
    # only show todos of the current user
    current_user = get_jwt_identity() # gets user_id from JWT
    todos = Todo.query.filter_by(user_id=current_user) 
    jsonified_todos = [todo.to_dict() for todo in todos]
    return render_template("home.html", todos=jsonified_todos, username=username)


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

    session["username"] = username

    # check if user is in the db, if not give an error
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return render_template("login.html", error="User not found")
    
    access_token = create_access_token(identity=str(user.id))
    resp = make_response(redirect(url_for("home")))
    set_access_cookies(resp, access_token) # places jwt cookie in users browser
    return resp
 

@app.route("/logout", methods=["GET", "POST"])
def logout():
    resp = make_response(redirect(url_for("login")))
    unset_access_cookies(resp)  
    return resp


@app.route("/create_todo", methods=["GET", "POST"])
@jwt_required()
def create_todo():
    if request.method == "GET":
        return render_template("create_todo.html")

    current_user_id = get_jwt_identity()

    name = request.form.get("form_name") 
    description = request.form.get("form_description")
    due_date = request.form.get("form_due_date")
    created_at = datetime.now().strftime("%Y-%m-%d")

    if not name:
        return render_template("create_todo.html", error="Name is required")
        
    new_todo = Todo()
    new_todo.user_id = current_user_id
    new_todo.name = name
    new_todo.description = description or ""
    new_todo.created_at = created_at
    new_todo.due_date = due_date or ""
    new_todo.status = "todo"
    
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))
