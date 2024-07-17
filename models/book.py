from init import db, ma
from marshmallow import fields

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)

    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)

    clubs = db.relationship("Club", back_populates="books")

class BookSchema(ma.Schema):

    clubs = fields.List(fields.Nested("ClubSchema", only=["name"]))

    class Meta:
        fields = ("id", "title", "author", "genre", "summary", "clubs")
        ordered = True

book_schema = BookSchema()

books_schema = BookSchema(many=True)