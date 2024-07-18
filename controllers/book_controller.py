from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.book import Book, book_schema, books_schema

book_bp = Blueprint("book", __name__, url_prefix="/book")

@book_bp.route("/", methods=["POST"])
def create_book():
    body_data = request.get_json()

    book = Book(
        title=body_data.get("title"),
        author=body_data.get("author"),
        genre=body_data.get("genre"),
        summary=body_data.get("summary")
    )

    db.session.add(book)
    db.session.commit()

    return book_schema.dump(book), 201

@book_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {"message": f"'{book.title}' book deleted successfully"}
    else:
        return {"error": f"Book with ID {book_id} not found"}, 404
    
@book_bp.route("/<int:book_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_book(book_id):
    body_data = request.get_json()
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        book.title = body_data.get("title") or book.title
        book.author = body_data.get("author") or book.author
        book.genre = body_data.get("genre") or book.genre
        book.summary = body_data.get("summary") or book.summary
        db.session.commit()
        return book_schema.dump(book)
    else:
        return {"error": f"Book with ID {book_id} not found"}, 404