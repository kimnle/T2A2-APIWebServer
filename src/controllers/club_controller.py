from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.club import Club, club_schema, clubs_schema
from utils import authorise_as_admin

club_bp = Blueprint("club", __name__, url_prefix="/club")

# /club - GET all clubs
@club_bp.route("/")
def get_all_clubs():
    # SELECT * FROM clubs;
    stmt = db.select(Club)
    clubs = db.session.scalars(stmt)

    # Return a response
    return clubs_schema.dump(clubs)

# /club/<id> - GET a single club
@club_bp.route("/<int:club_id>")
def get_one_club(club_id):
    # SELECT * FROM clubs WHERE id=club_id;
    stmt = db.select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)

    # If the club exists
    if club:
        # Return a response
        return club_schema.dump(club)
    
    # Else
    else:
        # Return an error
        return {"error": f"Club with ID {club_id} not found"}, 404

# /club - POST/create a new club
@club_bp.route("/", methods=["POST"])
@jwt_required()
def create_club():
    # Get the data from the body of the request
    body_data = request.get_json()

    # Create an instance of the Club model
    club = Club(
        name=body_data.get("name"),
        description=body_data.get("description"),
        updated=date.today(),
        user_id=get_jwt_identity()
    )

    # Add and commit to the DB
    db.session.add(club)
    db.session.commit()

    # Return a response
    return club_schema.dump(club)

# /club/<id> - DELETE a club
@club_bp.route("/<int:club_id>", methods=["DELETE"])
@jwt_required()
def delete_club(club_id):
    # SELECT * from club WHERE id=club_id;
    stmt = db.Select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)

    # If the club exists
    if club:

        # Check whether the user is an admin or the owner of the club
        is_admin = authorise_as_admin()
        if not is_admin and str(club.user_id) != get_jwt_identity():
            return {"error", "User is not authorised to delete this club"}, 403
        
        # Delete and commit to the DB
        db.session.delete(club)
        db.session.commit()

        # Return a response
        return {"message": f"'{club.name}' book club deleted successfully"}
    
    # Else
    else:
        # Return an error
        return {"error": f"Club with ID {club_id} not found"}, 404

# /club/<id> - PUT, PATCH/update a club
@club_bp.route("/<int:club_id>", methods=["PUT", "PATCH"])
def update_club(club_id):
    # Get the data from the body of the request
    body_data = request.get_json()

    # SELECT * from club WHERE id=club_id;
    stmt = db.select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)

    # If the club exists
    if club:
        # Check whether the user is the owner of the club
        if str(club.user_id) != get_jwt_identity():
            return {"error": "User is not authorise to update this club"}, 403
        
        # Update the fields
        club.name = body_data.get("name") or club.name
        club.description = body_data.get("description") or club.description
        club.updated = date.today()

        # Commit to the DB
        db.session.commit()

        # Return a response
        return club_schema.dump(club)
    
    # Else
    else:
        # Return an error
        return {"error": f"Club with ID {club_id} not found"}, 404