from flask import render_template, redirect, url_for, request, session, make_response, jsonify, abort
from db import Todo, User, db
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_access_cookies
from app_setup import app


# routes
@app.route("/", methods=["GET", "POST"])
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
    
    # now status is always todo, must add logic to actually change this
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


# flask routes for handling todo panel operations
@app.route("/todos/<int:todo_id>", methods=["PATCH"])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if not str(todo.user_id) == str(get_jwt_identity()):
        abort(404)
    
    data = request.get_json() or {}

    # update fields
    for field in ("name", "description", "due_date", "status"):
        if field in data:
            # equivalent to todo.field = data[field]
            setattr(todo, field, data[field])
    
    db.session.commit()
    return jsonify(todo=todo.to_dict())
    

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if not str(todo.user_id) == str(get_jwt_identity()):
        abort(404)
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify(ok=True)

print(app.url_map)
