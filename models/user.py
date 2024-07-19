from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    club = db.relationship("Club", back_populates="user", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")

class UserSchema(ma.Schema):

    club = fields.List(fields.Nested("ClubSchema", only=["name"]))
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["user", "id", "book.id", "book.club_books"]))

    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "club", "reviews")
        ordered = True

user_schema = UserSchema(exclude=["password"])

users_schema = UserSchema(many=True, exclude=["password"])