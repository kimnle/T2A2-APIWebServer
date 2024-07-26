from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# Create accepted ratings
VALID_RATINGS = (1, 2, 3, 4, 5)

# Review model
class Review(db.Model):
    __tablename__ = "reviews"

    # Structure of table
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)

    # Establish foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    # Set relationships
    user = db.relationship("User", back_populates="reviews")
    book = db.relationship("Book", back_populates="reviews")

# Review schema
class ReviewSchema(ma.Schema):
    # Set fields to be shown from relationships
    user = fields.Nested("UserSchema", only=["name"])
    book = fields.Nested("BookSchema", exclude=["reviews"])

    # Define the validation criteria for rating using the accepted ratings above
    rating = fields.Integer(required=True, validate=OneOf(VALID_RATINGS, error="Must be between 1 to 5"))

    # Shows which fields are displayed
    class Meta:
        fields = ("id", "rating", "comment", "user", "book")
        ordered = True

# Create schemas for handling one and many reviews
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)