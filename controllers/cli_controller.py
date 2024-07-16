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
        )
    ]

    db.session.add_all(users)

    clubs = [
        Club(
            name="Tea Time Book Club",
            description="This isn't just any book club. Each month, we are choosing an amazing new book. One of the greatest thrills of my life has been finding new stories that bring me deeper into my own existence, or catapult me into a new world. I can't wait to read with you. Love, Dakota",
            updated=date.today(),
            user=users[1]
        ),
        Club(
            name="Library Science",
            description="Library Science will curate books that aren't on the typical bestseller lists in order to better highlight new voices, writers to watch, overlooked, or underrepresented stories - and for greater context, we will occasionally throw in a classic that might better inform contemporary work. We'll cover writers and books from all points of view to reinforce the truth that ALL books are for everyone... and that we often learn the most from the stories that aren't our own. Thanks for being here -- we're so excited to read with you.",
            updated=date.today(),
            user=users[2]
        ),
        Club(
            name="Service95 Book Club",
            description="Welcome to the Service95 Book Club. We are thrilled to have a space where we can share with each other the titles that mean the most to us, and together dive into the minds of some of the world's greatest authors. Each month we will discuss a book personally chosen by Dua, representing writing from across the globe. You're invited to read along with us, share your insights, and contribute your recommendations of the titles we should all know about.",
            updated=date.today(),
            user=users[3]
        ),
        Club(
            name="Reese's Book Club",
            description="Each month, Reese, our founder (and book-lover-in-chief) chooses a book with a woman at the center of the story. There's not a formula to the books we spotlight, and we like it that way. We make our choices thoughtfully and look for ways to deepen our connection to books, authors and ourselves.",
            updated=date.today(),
            user=users[4]
        )
    ]

    db.session.add_all(clubs)

    db.session.commit()

    print("Tables seeded")