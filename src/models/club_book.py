from init import db, ma
from marshmallow import fields

# ClubBook model
class ClubBook(db.Model):
    __tablename__ = "club_books"

    # Structure of table
    id = db.Column(db.Integer, primary_key=True)

    # Establish foreign keys
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    # Set relationships
    club = db.relationship("Club", back_populates="club_books")
    book = db.relationship("Book", back_populates="club_books")

# ClubBook schema
class ClubBookSchema(ma.Schema):
    # Set fields to be shown from relationships
    club = fields.Nested("ClubSchema", only=["name"])
    book = fields.Nested("BookSchema", only=["title", "author"])

    # Shows which fields are displayed
    class Meta:
        fields = ("id", "club", "book")
        ordered = True

# Create schemas for handling one and many club books
club_book_schema = ClubBookSchema()
club_books_schema = ClubBookSchema(many=True)