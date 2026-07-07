from flask import Flask
from db import db
from flask_jwt_extended import JWTManager
import os
from pathlib import Path

# app setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["JWT_SECRET_KEY"] = "jwtsecretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

if os.path.exists("/.dockerenv"):
    database_uri = "sqlite:////app/data/task.db"
else:
    db_file = (Path(__file__).parent / "data" / "task.db").resolve()
    database_uri = f"sqlite:///{db_file.as_posix()}"

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

# initialize jwt authentication
jwt = JWTManager(app)

# initialize sqlalchemy
db.init_app(app)

from sqlalchemy import text

with app.app_context():
    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Engine URL:", db.engine.url)

# create new database every start, this is only for testing purposes
with app.app_context():
    db.create_all()
