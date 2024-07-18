from init import db, ma
from marshmallow import fields

class ClubBook(db.Model):
    __tablename__ = "club_books"

    id = db.Column(db.Integer, primary_key=True)

    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    club = db.relationship("Club", back_populates="club_books")
    book = db.relationship("Book", back_populates="club_books")

class ClubBookSchema(ma.Schema):

    club = fields.List(fields.Nested("ClubSchema"), only=["name"])
    book = fields.List(fields.Nested("BookSchema"), only=["title", "author"])

    class Meta:
        fields = ("id", "club", "book")
        ordered = True

club_book_schema = ClubBookSchema()

club_books_schema = ClubBookSchema(many=True)