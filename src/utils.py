from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User

def authorise_as_admin():
    # Get the user's ID from get_jwt_identity
    user_id = get_jwt_identity()

    # SELECT * FROM users WHERE id=user_id;
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # Check whether the user is an admin or not
    return user.is_admin