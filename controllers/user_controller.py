from flask import Blueprint

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/register")

@user_bp.route("user/login")