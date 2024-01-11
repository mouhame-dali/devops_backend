import json
from flask_cors import CORS
from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
app = Flask(__name__)
CORS(app)
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://mohamed:med.ALI123@localhost:5432/testdb"
db.init_app(app)

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    firstName: Mapped[str] = mapped_column(String)
    lastName: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [
            {
                "id": user.id, 
                "firstName": user.firstName, 
                "lastName": user.lastName, 
                "phone": user.phone,
                "country": user.country,
                "email": user.email,
                "image": user.image
            } 
            for user in users]
    return jsonify({"status": "error", "users": user_list}), 200

@app.route("/user", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        record = json.loads(request.data)
        user = User(
            firstName=record['firstName'],
            lastName=record['lastName'],
            phone=record['phone'],
            country=record['country'],
            email=record['email'],
            image=record['image'],
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "success", "message": "success"}), 201
    else:
        if request.args:
            user_id = request.args.get('id')
            user = User.query.filter_by(id=user_id).first()
            return jsonify({"status": "success", "user": {
                "id":user.id,
                "firstName":user.firstName,
                "lastName":user.lastName,
                "phone":user.phone,
                "country":user.country,
                "email":user.email,
                "image":user.image
            }}), 200