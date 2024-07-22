from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp

VALID_GENRES = ("Fiction", "Non-fiction")

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)

    club_books = db.relationship("ClubBook", back_populates="book", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete")

class BookSchema(ma.Schema):

    club_books = fields.List(fields.Nested("ClubBookSchema", exclude=["book", "id"]))
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["book", "id"]))

    author = fields.String(required=True, validate=Regexp("^[a-zA-Z ]*$", error="Must be alphabet characters only"))
    
    genre = fields.String(required=True, validate=OneOf(VALID_GENRES, error="Must be 'Fiction' or 'Non-fiction'"))

    class Meta:
        fields = ("id", "title", "author", "genre", "summary", "club_books", "reviews")
        ordered = True

book_schema = BookSchema()

books_schema = BookSchema(many=True)