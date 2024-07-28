from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.user import User, user_schema, users_schema, UserSchema
from utils import authorise_as_admin

user_bp = Blueprint("user", __name__, url_prefix="/user")

# /user - GET all users
@user_bp.route("/", methods=["GET"])
def get_all_users():
    # SELECT * FROM users;
    stmt = db.select(User)
    users = db.session.scalars(stmt)

    # Return a response
    return users_schema.dump(users)

# /user/<id> - GET a single user
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    # SELECT * FROM users WHERE id=user_id;
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # If the user exists
    if user:
        # Return a response
        return user_schema.dump(user)
    
    # Else
    else:
        # Return an error
        return {"error": f"User with ID {user_id} not found"}, 404

# /user/register - POST/create a new user
@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # Get the data from the body of the request
        body_data = UserSchema().load(request.get_json())

        # Create an instance of the User model
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )

        # Extract the password from the body
        password=body_data.get("password")

        # Hash the password
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Add and commit to the DB
        db.session.add(user)
        db.session.commit()

        # Return a response
        return user_schema.dump(user), 201
    
    # Handle possible integrity errors
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} field is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "The email address is already registered"}, 409

# /user/login - POST/login user
@user_bp.route("/login", methods=["POST"])
def login_user():
    # Get the data from the body of the request
    body_data = request.get_json()

    # SELECT * FROM users WHERE email="email";
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    # If the user exists and the password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # Create JWT
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=14))

        # Return a response
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    
    # Else
    else:
        # Return an error
        return {"error": "Invalid email or password"}, 401

# /user/<id> - DELETE a user
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    # SELECT * FROM users WHERE id=user_id;
    stmt = db.Select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # If the user exists
    if user:
        # Check whether the user is an admin or the owner of the account
        is_admin = authorise_as_admin()
        if not is_admin and str(user_id) != get_jwt_identity():
            return {"error": "User is not authorised to delete this user"}, 403
        
        # Delete and commit to the DB
        db.session.delete(user)
        db.session.commit()

        # Return a response
        return {"message": f"'{user.name}' user deleted successfully"}
    
    # Else
    else:
        # Return an error
        return {"error": f"User with ID {user_id} not found"}, 404

# /user/<id> - PUT, PATCH/update a user
@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(user_id):
    # Get the data from the body of the request
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")

    # SELECT * FROM users WHERE user_id=Integer;
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # If the user exists
    if user:
        # Check whether the user is the owner of the account
        if str(user_id) != get_jwt_identity():
            return {"error": "User is not authorised to update this user"}, 403
        
        # Update the fields
        user.name = body_data.get("name") or user.name
        user.email = body_data.get("email") or user.email
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        # Commit to the DB
        db.session.commit()

        # Return a response
        return user_schema.dump(user)
    
    # Else
    else:
        # Return an error
        return {"error": f"User with ID {user_id} not found"}, 404