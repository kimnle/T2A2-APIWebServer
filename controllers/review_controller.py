from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.book import Book

review_bp = Blueprint("review", __name__, url_prefix="/<int:book_id>/review")

@review_bp.route("/", methods=["POST"])
@jwt_required
def create_review(book_id):
    body_data = request.get_json()
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        review = Review(
            rating=body_data.get("rating"),
            comment=body_data.get("comment"),
            book=book,
            user=get_jwt_identity()
        )
        db.session.add(review)
        db.session.commit()
        return review_schema.dump(review), 201
    else:
        return {"error": f"Book with ID {book_id} not found"}, 404