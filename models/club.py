from init import db, ma
from marshmallow import fields

# Club model
class Club(db.Model):
    __tablename__ = "clubs"

    # Structure of table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    updated = db.Column(db.Date)

    # Establish foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Set relationships
    user = db.relationship("User", back_populates="club")
    club_books = db.relationship("ClubBook", back_populates="club", cascade="all, delete")

# Club schema
class ClubSchema(ma.Schema):
    # Set fields to be shown from relationships
    user = fields.Nested("UserSchema", only=["name"])
    club_books = fields.List(fields.Nested("ClubBookSchema", exclude=["club", "id"]))

    # Shows which fields are displayed
    class Meta:
        fields = ("id", "name", "description", "updated", "user", "club_books")
        ordered = True
        
# Create schemas for handling one and many clubs
club_schema = ClubSchema()
clubs_schema = ClubSchema(many=True)