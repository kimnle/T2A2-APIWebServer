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
        return {"error": f"Club with id {club_id} not found"}, 404
    
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