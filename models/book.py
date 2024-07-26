from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp

# Created accepted genres
VALID_GENRES = ("Fiction", "Non-fiction")

# Book model
class Book(db.Model):
    __tablename__ = "books"

    # Structure of table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)

    # Set relationships
    club_books = db.relationship("ClubBook", back_populates="book", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete")

# Book schema
class BookSchema(ma.Schema):
    # Set fields to be shown from relationships
    club_books = fields.List(fields.Nested("ClubBookSchema", exclude=["book", "id"]))
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["book"]))

    # Define the validation criteria for author
    author = fields.String(required=True, validate=Regexp("^[a-zA-Z ]*$", error="Must be alphabet characters only"))
    
    # Define the validation criteria for genre using the accepted genres above
    genre = fields.String(required=True, validate=OneOf(VALID_GENRES, error="Must be 'Fiction' or 'Non-fiction'"))

    # Shows which fields are displayed
    class Meta:
        fields = ("id", "title", "author", "genre", "summary", "club_books", "reviews")
        ordered = True

# Create schemas for handling one and many books
book_schema = BookSchema()
books_schema = BookSchema(many=True)