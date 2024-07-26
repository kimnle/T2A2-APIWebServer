from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

# User model
class User(db.Model):
    __tablename__ = "users"

    # Structure of table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Set relationships
    club = db.relationship("Club", back_populates="user", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")

# User schema
class UserSchema(ma.Schema):
    # Set fields to be shown from relationships
    club = fields.List(fields.Nested("ClubSchema", only=["name"]))
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["user", "id", "book.id", "book.club_books"]))

    # Define the validation criteria for name
    name = fields.String(required=True, validate=Regexp("^[a-zA-Z ]*$", error="Must be alphabet characters only"))

    # Define the validation criteria for email
    email = fields.String(required=True, validate=Regexp("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", error="Invalid email format"))

    # Define the validation criteria for password
    password = fields.String(required=True, validate=Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", error="Must be minimum eight characters with at least one uppercase letter, one lowercase letter, one number and one special character"))

    # Shows which fields are displayed
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "club", "reviews")
        ordered = True

# Create schemas for handling one and many users
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])