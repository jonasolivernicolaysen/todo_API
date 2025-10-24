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
    return render_template("index.html")
    
@app.get("/health")
def health():
    return {"status": "ok"}
