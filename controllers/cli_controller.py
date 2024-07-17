from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.club import Club
from models.book import Book

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

    books = [
        Book(
            title="Pink Slime",
            author="Fernanda Trias",
            genre="Fiction",
            summary="A port city is in the grips of an ecological crisis. The river has filled with toxic algae, and a deadly 'red wind' blows through its streets; much of the coast has been evacuated as the wealthy migrate inland to safety, leaving the rest to shelter in abandoned houses as blackouts and food shortages abound. The unnamed narrator is one of those who has stayed. She spends her days trying to disentangle herself from the two relationships that had once meant everything to her, and looking after the young boy who's been placed in her care. As the world in which they move becomes smaller, she reflects on the collapse of the other emotional ties in her life and the emergence of a radical yet tender solitude.",
            club=clubs[0]
        ),
        Book(
            title="We Were the Universe",
            author="Kimberly King Parsons",
            genre="Fiction",
            summary="The trip was supposed to be fun. When Kit's best friend gets dumped by his boyfriend, he begs her to ditch her family responsibilities for a quick, idyllic weekend away. They'll soak in hot springs, then drink too much, like old times. Instead, their getaway only reminds Kit of everything she's lost lately: her wildness, her independence and - most heartbreakingly of all - her sister, Julie, who died a few years ago. When she returns home, Kit tries to settle the routine of caring for her irrepressible young daughter. But in the secret recesses of Kit's mind, she's fantasizing about the hot playground mum and reminiscing about the band she used to be in with her sister - and how they'd go out to the desert after shows and drop acid.Keyed into everything that might distract her from her surfacing grief, Kit begins to spiral, and as her already thin boundaries between reality and fantasty blur, she starts to wonder: is Julie really gone?",
            club=clubs[0]
        ),
        Book(
            title="JOB",
            author="Max Wolf Friedlich",
            genre="Fiction",
            summary="Jane, an employee at the big tech company (you know the one), has been placed on leave after becoming the subject of a viral video. She arrives in the office of a crisis therapist - Loyd - determined to be reinstated to the job that gives her life meaning.",
            club=clubs[1]
        ),
        Book(
            title="Role Play",
            author="Clara Drummond",
            genre="Fiction",
            summary="Vivian is a curator, not just at her gallery gig in Rio de Janeiro, but in every aspect of her life. Her apartment has designer armchairs. Her wallet is Comme des Garçons. Everything is selected and arranged, even her lovers and friends. In Vivian's world, everything comes in excess, including her own caustic selfawareness. As she informs us, 'I'm a misandrist and a misogynist,' but she is fond of gay men, 'the one type of human you can properly get along with as equals.'",
            club=clubs[1]
        ),
        Book(
            title="Noughts & Crosses",
            author="Malorie Blackman",
            genre="Fiction",
            summary="Two young people are forced to make a stand in this thought-provoking look at racism and prejudice in an alternate society. Sephy is a Cross -- a member of the dark-skinned ruling class. Callum is a Nought -- a 'colourless' member of the underclass who were once slaves to the Crosses. The two have been friends since early childhood, but that's as far as it can go. In their world, Noughts and Crosses simply don't mix. Against a background of prejudice and distrust, intensely highlighted by violent terrorist activity, a romance builds between Sephy and Callum -- a romance that is to lead both of them into terrible danger. Can they possibly find a way to be together?",
            club=clubs[2]
        ),
        Book(
            title="Say Nothing",
            author="Patrick Radden Keefe",
            genre="Non-fiction",
            summary="In December 1972, Jean McConville, a thirty-eight-year-old mother of ten, was dragged from her Belfast home by masked intruders, her children clinging to her legs. They never saw her again. Her abduction was one of the most notorious episodes of the vicious conflict known as The Troubles. Everyone in the neighborhood knew the I.R.A. was responsible. But in a climate of fear and paranoia, no one would speak of it. In 2003, five years after an accord brought an uneasy peace to Northern Ireland, a set of human bones was discovered on a beach. McConville's children knew it was their mother when they were told a blue safety pin was attached to the dress--with so many kids, she had always kept it handy for diapers or ripped clothes.",
            club=clubs[2]
        ),
        Book(
            title="The Cliffs",
            author="J. Courtney Sullivan",
            genre="Fiction",
            summary="On a secluded bluff overlooking the ocean sits a Victorian house, lavender with gingerbread trim, a home that contains a century's worth of secrets. By the time Jane Flanagan discovers the house as a teenager, it has long been abandoned. The place is an irresistible mystery to Jane. There are still clothes in the closets, marbles rolling across the floors, and dishes in the cupboards, even though no one has set foot there in decades. The house becomes a hideaway for Jane, a place to escape her volatile mother. Twenty years later, now a Harvard archivist, she returns home to Maine following a terrible mistake that threatens both her career and her marriage. Jane is horrified to find the Victorian is now barely recognizable. The new owner, Genevieve, a summer person from Beacon Hill, has gutted it, transforming the house into a glossy white monstrosity straight out of a shelter magazine. Strangely, Genevieve is convinced that the house is haunted—perhaps the product of something troubling Genevieve herself has done. She hires Jane to research the history of the place and the women who lived there. The story Jane uncovers—of lovers lost at sea, romantic longing, shattering loss, artistic awakening, historical artifacts stolen and sold, and the long shadow of colonialism—is even older than Maine itself.",
            club=clubs[3]
        ),
        Book(
            title="The Unwedding",
            author="Ally Condie",
            genre="Fiction",
            summary="Ellery Wainwright is alone at the edge of the world. She and her husband, Luke, were supposed to spend their twentieth wedding anniversary together at the luxurious Resort at Broken Point in Big Sur, California. Where better to celebrate a marriage, a family, and a life together than at one of the most stunning places on earth? But now she's traveling solo. To add insult to injury, there's a wedding at Broken Point scheduled during her stay. Ellery remembers how it felt to be on the cusp of everything new and wonderful, with a loved and certain future glimmering just ahead. Now, she isn't certain of anything except for her love for her kids and her growing realization that this place, though beautiful, is unsettling. When Ellery discovers the body of the groom floating in the pool in the rain, she realizes that she is not the only one whose future is no longer guaranteed. Before the police can reach Broken Point, a mudslide takes out the road to the resort, leaving the guests trapped. When another guest dies, it's clear something horrible is brewing. Everyone at Broken Point has a secret. And everyone has a shadow. Including Ellery.",
            club=clubs[3]
        )
        Book(
            title="Long Island Compromise",
            author="Taffy Brodesser-Akner",
            genre="Fiction",
            summary="In 1980, a wealthy businessman named Carl Fletcher is kidnapped from his driveway, brutalized, and held for ransom. He is returned to his wife and kids less than a week later, only slightly the worse, and the family moves on with their lives, resuming their prized places in the saga of the American dream, comforted in the realization that though their money may have been what endangered them, it is also what assured them their safety. But now, nearly forty years later, it's clear that perhaps nobody ever got over anything, after all. Carl has spent the ensuing years secretly seeking closure to the matter of his kidnapping, while his wife, Ruth, has spent her potential protecting her husband's emotional health. Their three grown children aren't doing much better: Nathan's chronic fear won't allow him to advance at his law firm; Beamer, a Hollywood screenwriter, will consume anything—substance, foodstuff, women—in order to numb his own perpetual terror; and Jenny has spent her life so bent on proving that she's not a product of her family's pathology that she has come to define it. As they hover at the delicate precipice of a different kind of survival, they learn that the family fortune has dwindled to just about nothing, and they must face desperate questions about how much their wealth has played a part in both their lives' successes and failures.",
            club=clubs[0]
        )
    ]

    db.session.commit()

    print("Tables seeded")