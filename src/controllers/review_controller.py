from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.book import Book
from utils import authorise_as_admin

review_bp = Blueprint("review", __name__, url_prefix="/<int:book_id>/review")

# /book/<id>/review - POST/create a new review
@review_bp.route("/", methods=["POST"])
@jwt_required()
def create_review(book_id):
    # Get the data from the body of the request
    body_data = review_schema.load(request.get_json(), partial=True)

    # SELECT * FROM books WHERE id=book_id;
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)

    # If the book exists
    if book:
        # Create an instance of the Review model
        review = Review(
            rating=body_data.get("rating"),
            comment=body_data.get("comment"),
            book=book,
            user_id=get_jwt_identity()
        )

        # Add and commit to the DB
        db.session.add(review)
        db.session.commit()

        # Return a response
        return review_schema.dump(review), 201
    
    # Else
    else:
        # Return an error
        return {"error": f"Book with ID {book_id} not found"}, 404

# /book/<id>/review/<id> - DELETE a review
@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(book_id, review_id):
    # SELECT * FROM reviews WHERE id=review_id
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    # If the review exists
    if review:
        # Check whether the user is an admin or owner of the review
        is_admin = authorise_as_admin()
        if not is_admin and str(review.user_id) != get_jwt_identity():
            return {"error": "User not authorised to delete this review"}, 403
        
        # Delete and commit to DB
        db.session.delete(review)
        db.session.commit()

        # Return a response
        return {"message": "Review deleted successfully"}
    
    # Else
    else:
        # Return an error
        return {"error": f"Review with ID {review_id} not found"}, 404