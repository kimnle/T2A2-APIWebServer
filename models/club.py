from init import db, ma
from marshmallow import fields

class Club(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    updated = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="club")
    books = db.relationship("Book", back_populates="clubs")

class ClubSchema(ma.Schema):

    user = fields.Nested("UserSchema", only=["name"])
    books = fields.List(fields.Nested("BookSchema", only=["title", "author"]))

    class Meta:
        fields = ("id", "name", "description", "updated", "user", "books")
        ordered = True

club_schema = ClubSchema()

clubs_schema = ClubSchema(many=True)