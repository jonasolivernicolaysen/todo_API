from flask import Flask
from db import db
from flask_jwt_extended import JWTManager

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