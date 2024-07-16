from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.club import Club

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            name="Admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin=True
        ),
        User(
            name="Dakota Johnson",
            email="dakotajohnson@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8")
        ),
        User(
            name="Kaia Gerber",
            email="kaiagerber@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8")
        ),
        User(
            name="Dua Lipa",
            email="dualipa@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8")
        ),
        User(
            name="Reese Witherspoon",
            email="reesewitherspoon@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8")
        ),
        User(
            name="Emma Roberts",
            email="emmaroberts@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8")
        )
    ]

    db.session.add_all(users)

    clubs = [
        Club(
            name="Tea Time Book Club",
            description="This isn't just any book club. Each month, we are choosing an amazing new book, and when you sign up to our channel we will send you down a rabbit hole. As we sink into the depths of each story, you will receive links, playlists, author exclusives, messages and videos from me and MUCH more. One of the greatest thrills of my life has been finding new stories that bring me deeper into my own existence, or catapult me into a new world. I can't wait to read with you. Love, Dakota",
            updated=date.today(),
            user=users[1]
        )
    ]

    db.session.commit()

    print("Tables seeded")