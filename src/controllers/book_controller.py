from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.book import Book, book_schema, books_schema
from controllers.review_controller import review_bp
from models.club_book import ClubBook, club_book_schema
from models.club import Club
from models.user import User
from utils import authorise_as_admin

book_bp = Blueprint("book", __name__, url_prefix="/book")
book_bp.register_blueprint(review_bp)

# /book - GET all books
@book_bp.route("/")
def get_all_books():
    # SELECT * FROM books;
    stmt = db.select(Book)
    books = db.session.scalars(stmt)

    # Return a response
    return books_schema.dump(books)

# /book/<id> - GET a single book
@book_bp.route("/<int:book_id>")
def get_one_book(book_id):
    # SELECT * FROM books WHERE id=book_id;
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)

    # If the books exists
    if book:
        # Return a response
        return book_schema.dump(book)
    
    # Else
    else:
        # Return an error
        return {"error": f"Book with ID {book_id} not found"}, 404

# /book - POST/create a new book
@book_bp.route("/", methods=["POST"])
def create_book():
    # Get the data from the body of the request
    body_data = book_schema.load(request.get_json())

    # Create an instance of the Book model
    book = Book(
        title=body_data.get("title"),
        author=body_data.get("author"),
        genre=body_data.get("genre"),
        summary=body_data.get("summary")
    )

    # Add and commit to the DB
    db.session.add(book)
    db.session.commit()

    # Return a response
    return book_schema.dump(book), 201

# /book/<id> - DELETE a book
@book_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    # SELECT * FROM books WHERE id=book_id;
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)

    # If the book exists
    if book:
        # Check whether the user is an admin
        is_admin = authorise_as_admin()
        if not is_admin:
            return {"error": "User not authorised to delete a book"}, 403
        
        # Delete and commit to the DB
        db.session.delete(book)
        db.session.commit()

        # Return a response
        return {"message": f"'{book.title}' book deleted successfully"}
    
    # Else
    else:
        # Return an error
        return {"error": f"Book with ID {book_id} not found"}, 404

# /book/<id> - PUT, PATCH/update a book
@book_bp.route("/<int:book_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_book(book_id):
    # Get the data from the body of the request
    body_data = book_schema.load(request.get_json(), partial=True)

    # SELECT * FROM books WHERE id=book_id
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)

    # If the book exists
    if book:
        # Check whether the user is an admin
        is_admin = authorise_as_admin()
        if not is_admin:
            return {"error": "User not authorised to update a book"}, 403
        
        # Update the fields
        book.title = body_data.get("title") or book.title
        book.author = body_data.get("author") or book.author
        book.genre = body_data.get("genre") or book.genre
        book.summary = body_data.get("summary") or book.summary

        # Commit to the DB
        db.session.commit()

        # Return a response
        return book_schema.dump(book)
    
    # Else
    else:
        # Return an error
        return {"error": f"Book with ID {book_id} not found"}, 404

# /book/<id>/club/<id> - POST/assign a book to a club
@book_bp.route("/<int:book_id>/club/<int:club_id>", methods=["POST"])
@jwt_required()
def assign_club_book(book_id, club_id):
    # SELECT * FROM clubs WHERE id=club_id;
    stmt = db.select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)

    # If the club exists
    if club:
        # Check whether the user is the owner of the club
        if str(club.user_id) == get_jwt_identity():
            # Create an instance of the Club Book model
            club_book = ClubBook(
                book_id=book_id,
                club_id=club_id
            )

            # Add and commit to the DB
            db.session.add(club_book)
            db.session.commit()

            # Return a response
            return club_book_schema.dump(club_book), 201
        
        # Else
        else:
            # Return an error
            return {"error": "User is not authorised to assign the book to this club"}, 403

    # Else
    else:
        # Return an error
        return {"error": f"Club with ID {club_id} not found"}, 404

# /book/<id>/<club/<id> - DELETE a book from a club
@book_bp.route("/<int:book_id>/club/<int:club_id>", methods=["DELETE"])
@jwt_required()
def delete_club_book(book_id, club_id):
    # SELECT * from club_books WHERE club_books.book_id = book_id and club_books.club_id = club_id;
    stmt = db.select(ClubBook).where(ClubBook.book_id == book_id and ClubBook.club_id == club_id)
    club_book = db.session.scalar(stmt)

    # SELECT * FROM books WHERE id=book_id;
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)

    # SELECT * FROM clubs WHERE id=club_id;
    stmt = db.select(Club).filter_by(id=club_id)
    club = db.session.scalar(stmt)

    # If the assignment exists
    if club_book:
        # Check where the user is the owner of the club
        if str(club.user_id) != get_jwt_identity():
            return {"error": "User is not authorised to delete the book from this club"}, 403
        
        # Delete and commit to the DB
        db.session.delete(club_book)
        db.session.commit()

        # Return a response
        return {"message": f"'{book.title}' book deleted from '{club.name}' successfully"}
    
    # Else
    else:
        # Return an error
        return {"error": f"Book with ID {book_id} is not in club with ID {club.id}"}, 404