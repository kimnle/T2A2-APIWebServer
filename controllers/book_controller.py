from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.book import Book, book_schema, books_schema
from controllers.review_controller import review_bp
from models.club_book import ClubBook, club_book_schema
from models.club import Club

book_bp = Blueprint("book", __name__, url_prefix="/book")
book_bp.register_blueprint(review_bp)

@book_bp.route("/")
def get_all_books():
    stmt = db.select(Book)
    books = db.session.scalars(stmt)
    return books_schema.dump(books)

@book_bp.route("/<int:book_id>")
def get_one_book(book_id):
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        return book_schema.dump(book)
    else:
        return {"error": f"Book with ID {book_id} not found"}, 404

@book_bp.route("/", methods=["POST"])
def create_book():
    body_data = book_schema.load(request.get_json())

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
    body_data = book_schema.load(request.get_json(), partial=True)
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
    
@book_bp.route("/<int:book_id>/club/<int:club_id>", methods=["POST"])
@jwt_required()
def assign_club_book(book_id, club_id):
    club_book = ClubBook(
        book_id=book_id,
        club_id=club_id
    )
    db.session.add(club_book)
    db.session.commit()
    return club_book_schema.dump(club_book), 201

@book_bp.route("/<int:book_id>/club/<int:club_id>", methods=["DELETE"])
@jwt_required()
def delete_club_book(book_id, club_id):
    stmt = db.select(ClubBook).where(ClubBook.book_id == book_id and ClubBook.club_id == club_id)
    club_book = db.session.scalar(stmt)

    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)

    stmt = db.select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)

    if club_book:
        db.session.delete(club_book)
        db.session.commit()
        return {"message": f"'{book.title}' book deleted from '{club.name}' successfully"}
    else:
        return {"error": f"Book with ID {book_id} is not in club with ID {club.id}"}