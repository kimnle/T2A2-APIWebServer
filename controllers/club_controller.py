from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.club import Club, club_schema, clubs_schema

club_bp = Blueprint("club", __name__, url_prefix="/club")

@club_bp.route("/")
def get_all_clubs():
    stmt = db.select(Club)
    clubs = db.session.scalars(stmt)
    return clubs_schema.dump(clubs)

@club_bp.route("/<int:club_id>")
def get_one_club(club_id):
    stmt = db.select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)
    if club:
        return club_schema.dump(club)
    else:
        return {"error": f"Club with ID {club_id} not found"}, 404
    
@club_bp.route("/", methods=["POST"])
@jwt_required()
def create_club():
    body_data = request.get_json()

    club = Club(
        name=body_data.get("name"),
        description=body_data.get("description"),
        updated=date.today(),
        user_id=get_jwt_identity()
    )

    db.session.add(club)
    db.session.commit()

    return club_schema.dump(club)

@club_bp.route("/<int:club_id>", methods=["DELETE"])
@jwt_required()
def delete_club(club_id):
    stmt = db.Select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)
    if club:
        db.session.delete(club)
        db.session.commit()
        return {"message": f"{club.name} deleted successfully"}
    else:
        return {"error": f"Club with ID {club_id} not found"}, 404
    
@club_bp.route("/<int:club_id>", methods=["PUT", "PATCH"])
def update_club(club_id):
    body_data = request.get_json()
    stmt = db.select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)
    if club:
        club.name = body_data.get("name") or club.name
        club.description = body_data.get("description") or club.description
        club.updated = date.today()
        db.session.commit()
        return club_schema.dump(club)
    else:
        return {"error": f"Club with ID {club_id} not found"}, 404