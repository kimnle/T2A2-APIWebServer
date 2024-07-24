from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.user import User, user_schema, users_schema, UserSchema
from utils import authorise_as_admin

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/", methods=["GET"])
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return users_schema.dump(users)

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return user_schema.dump(user)
    else:
        return {"error": f"User with ID {user_id} not found"}, 404

@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body_data = UserSchema().load(request.get_json())

        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )
        password=body_data.get("password")

        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} field is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "The email address is already registered"}, 409

@user_bp.route("/login", methods=["POST"])
def login_user():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=14))
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    
    else:
        return {"error": "Invalid email or password"}, 401
    
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    stmt = db.Select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        is_admin = authorise_as_admin()
        if not is_admin and str(user_id) != get_jwt_identity():
            return {"error": "Not authorised to delete this user"}, 403
        db.session.delete(user)
        db.session.commit()
        return {"message": f"'{user.name}' user deleted successfully"}
    else:
        return {"error": f"User with ID {user_id} not found"}, 404
    
@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(user_id):
    body_data = UserSchema().load(request.get_json(), partial=True)
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    password = body_data.get("password")
    if user:
        if str(user_id) != get_jwt_identity():
            return {"error": "Not authorised to update this user"}, 403
        user.name = body_data.get("name") or user.name
        user.email = body_data.get("email") or user.email
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        db.session.commit()
        return user_schema.dump(user)
    else:
        return {"error": f"User with ID {user_id} not found"}, 404