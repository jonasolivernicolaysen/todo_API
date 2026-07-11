from flask import render_template, redirect, url_for, request, session, make_response, jsonify, abort
from db import Task, User, db
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_access_cookies
from app_setup import app
from AuthService import hashPassword, checkPassword
from sqlalchemy import case
from statuses import Status


# routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    # ensure all fields exist
    if username is None or password is None:
        return render_template("login.html")

    # check if user is in the db, if not give an error
    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template("login.html", error="User not found")
    user_password = user.password

    password_exists = checkPassword(password, user_password)
    if not password_exists:
        return render_template("login.html", error="Incorrect password")
    
    session["username"] = username

    access_token = create_access_token(identity=str(user.id))
    resp = make_response(redirect(url_for("home")))
    set_access_cookies(resp, access_token) # places jwt cookie in users browser
    return resp
 

@app.route("/home", methods=["GET", "POST"])
@jwt_required()
def home():
    username = session.get("username")
    return render_template("home.html", username=username, Status=Status)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":   
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    password_check = request.form.get("password_check")

    # ensure all fields exist
    if username is None or password is None or password_check is None:
        return render_template("register.html")
    
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("register.html", error="Username already taken")

    if password != password_check:
        return render_template("register.html", error="Passwords must match")
    
    new_user = User()
    new_user.username = username
    new_user.password = hashPassword(password=password)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    resp = make_response(redirect(url_for("login")))
    unset_access_cookies(resp)  
    return resp


@app.route("/create_task", methods=["GET", "POST"])
@jwt_required()
def create_task():
    if request.method == "GET":
        return render_template("create_task.html")

    current_user_id = get_jwt_identity()

    title = request.form.get("form_title") 
    description = request.form.get("form_description")
    due_date = request.form.get("form_due_date")
    created_at = datetime.now().strftime("%Y-%m-%d")

    if not title:
        return render_template("create_task.html", error="Title is required")
    
    new_task = Task()
    new_task.user_id = current_user_id
    new_task.title = title
    new_task.description = description or ""
    new_task.created_at = created_at
    new_task.due_date = due_date or ""
    new_task.status = Status.TODO.value
    
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))


# flask routes for handling task panel operations
@app.route("/tasks/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    if not str(task.user_id) == str(get_jwt_identity()):
        abort(404)
    
    data = request.get_json() or {}

    # update fields
    for field in ("title", "description", "due_date", "status"):
        if field in data:
            setattr(task, field, data[field])
    
    db.session.commit()
    return jsonify(task=task.to_dict())
    

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not str(task.user_id) == str(get_jwt_identity()):
        abort(404)
    
    db.session.delete(task)
    db.session.commit()
    return jsonify(ok=True)

@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    # only show tasks of the current user
    current_user = get_jwt_identity() # gets user_id from JWT
    tasks = Task.query.filter_by(user_id=current_user).order_by(
        case(
            (Task.status == Status.TODO.value, 0),
            (Task.status == Status.DOING.value, 1),
            (Task.status == Status.DONE.value, 2)
        )
    )
    jsonified_tasks = [task.to_dict() for task in tasks]
    return jsonify(tasks=jsonified_tasks)

print(app.url_map)
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
        )
