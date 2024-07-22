from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.book import Book

review_bp = Blueprint("review", __name__, url_prefix="/<int:book_id>/review")

@review_bp.route("/", methods=["POST"])
@jwt_required()
def create_review(book_id):
    body_data = review_schema.load(request.get_json(), partial=True)
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        review = Review(
            rating=body_data.get("rating"),
            comment=body_data.get("comment"),
            book=book,
            user_id=get_jwt_identity()
        )
        db.session.add(review)
        db.session.commit()
        return review_schema.dump(review), 201
    else:
        return {"error": f"Book with ID {book_id} not found"}, 404
    
@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(book_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted successfully"}
    else:
        return {"error": f"Review with ID {review_id} not found"}, 404