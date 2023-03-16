from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password, category):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.category = category

    def __repr__(self):
        return f"<User id: {self.id}, username: {self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Character(db.Model):
    __tablename__ = "characters"

    character_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String)
    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    status = db.Column(db.String, nullable=False, default="Avaliable")
    booked = db.Column(db.Boolean, default=False, nullable=False)
    booked_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)

    booked_by = db.relationship(
        "User", backref="booked_characters", foreign_keys=[booked_by_id])
    created_by = db.relationship(
        "User", backref="created_characters", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<Character id: {self.character_id}, character name: {self.name}>"


class Request(db.Model):
    __tablename__ = "requests"

    request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String)
    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    status = db.Column(db.String, nullable=False, default="Avaliable")
    booked = db.Column(db.Boolean, default=False, nullable=False)
    booked_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)

    booked_by = db.relationship(
        "User", backref="booked_requests", foreign_keys=[booked_by_id])
    created_by = db.relationship(
        "User", backref="created_requests", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<Request id: {self.request_id}, request title: {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag id: {self.tag_id}, tag name: {self.name}>"


class Rating(db.Model):
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey(
        "requests.request_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    users = db.relationship("User", backref="ratings")
    requests = db.relationship("Request", backref="ratings")

    def __repr__(self):
        return f"<Rating id: {self.rating_id}, score: {self.score}>"


class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    request_id = db.Column(db.Integer, db.ForeignKey(
        "requests.request_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    users = db.relationship("User", backref="comments")
    requests = db.relationship("Request", backref="comments")

    def __repr__(self):
        return f"<Comment id: {self.comment_id}, comment text: {self.text}>"


class Request_Character(db.Model):
    __tablename__ = "requests-characters"

    rc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey(
        "requests.request_id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey(
        "characters.character_id"), nullable=False)

    request = db.relationship("Request", backref="requests_characters")
    chracter = db.relationship("Character", backref="requests_characters")

    def __repr__(self):
        return f"<Id: {self.rc_id}>"


class Request_Tag(db.Model):
    __tablename__ = "requests-tags"

    rt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey(
        "requests.request_id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        "tags.tag_id"), nullable=False)

    tag = db.relationship("Tag", backref="requests_tags")
    request = db.relationship("Request", backref="requests_tags")

    def __repr__(self):
        return f"<Id: {self.rt_id}>"


def connect_to_db(flask_app):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = True
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
