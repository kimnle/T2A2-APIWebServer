# T2A2: API Webserver

## Problem that this app will solve, and how this app solves or addresses the problem

Celebrity book clubs have skyrocketed in popularity, wielding significant influence over readers. As a book enthusiast, I wholeheartedly support famous individuals using their platform to promote reading. However, the proliferation of these clubs makes it challenging to track which celebrities have book clubs, their book selections, and the reasons behind their choices.

This app addresses this issue by providing a centralised platform for accessing book club information. Instead of navigating multiple Instagram and website pages, users can find all the details in one place. Imagine trying to compare book selections across [11 different celebrity book clubs](https://www.today.com/popculture/books/celebrity-book-clubs-rcna143075) – this app simplifies this process.

Disclaimer: this app isn't just for celebrities, it's also for people who just want to share what they're reading and their take on the book.

## How tasks are allocated and tracked in your project

During the development of this project, I used Trello to track and manage my tasks. I created three lists:

* To Do

* Doing

* Done

To help structure the development process, I re-watched lessons on API development and outlined the steps as checklists within Trello cards. Each card was named after a file that needed to be created and labeled according to the folder it belonged to.

![Trello screenshot 1](/docs/trello-1.png)

![Trello screenshot 2](/docs/trello-2.png)

Initially, I placed all the cards in the To Do list. As I completed each subtask, I moved the corresponding card to the Doing list.

At some point during the development, I re-evaluated my ERD and realised I needed a join table. I added a card with the file's name but didn't include a checklist since the steps for model files are quite similar. Instead, I referred to the checklist on another card to complete the task.

![Trello screenshot 3](/docs/trello-8.png)

## Third-party services, packages and dependencies used in this app

### PostgreSQL

PostgreSQL is an object-relational database management system (ORDBMS) that effectively combines relational and object-oriented paradigms. This allows for the storage and manipulation of complex data structures within a relational framework. By leveraging PostgreSQL's object-oriented capabilities, developers can interact with the database using object-oriented constructs, enhancing code readability and maintainability. This application capitalises on PostgreSQL's robust relational features to comprehensively manage its data.

### Flask

Flask is a lightweight Python web framework that simplifies the creation of web applications. It provides essential tools for building web pages and handling user interactions. This application employs Flask to construct its API, allowing for efficient data exchange and management.

### SQLAlchemy

SQLAlchemy is a versatile Python toolkit for interacting with SQL databases. It bridges the gap between Python objects and relational data, enabling efficient database management. This application utilises SQLAlchemy to query, manipulate, and relate data, performing CRUD operations while ensuring data integrity and handling potential exceptions.

### Marshmallow

Marshmallow is a Python library specialising in data serialisation and deserialisation. It efficiently converts complex data structures into formats like JSON for storage or transmission. This application leverages Marshmallow to define data schemas, transform data into JSON, manage intricate data relationships, and ensure data integrity through rigorous validation.

### Psycopg2

Psycopg2 is a Python library that acts as a bridge between Python applications and PostgreSQL databases. It provides direct access to execute SQL commands, enabling efficient data interaction and management within this application.

### JWT Extended

Flask-JWT-Extended is a Python extension that simplifies JWT (JSON Web Token) authentication in Flask applications. By providing secure, stateless token management, it enhances application security. This application utilises Flask-JWT-Extended to generate and verify access tokens, safeguarding routes and authorising user actions.

### Bcrypt

Bcrypt is a robust cryptographic hash function specifically designed for securely storing passwords. It renders passwords unreadable by creating a complex hash value during registration. This hash, combined with a unique salt, is stored instead of the plain-text password. When a user attempts to log in, the provided password is hashed and compared to the stored hash, ensuring password security without exposing sensitive data.

### Dotenv

The dotenv package is a valuable tool for securely managing sensitive information like API keys and database credentials. By storing these values in a .env file outside of the codebase, it prevents accidental exposure through version control. This application utilises dotenv to isolate sensitive configuration details, enhancing security and maintainability.

## Benefits and drawbacks of this app's underlying database system

This app's database system is PostgreSQL.

### Benefits

Open source database: PostgreSQL is a free and open-source database that can be used, distributed, and modified without cost. A large community of developers supports its development, offers help, and maintains its documentation.

Object relational database features: PostgreSQL allows building complex structures within the database itself, just like in aprogramming language. Define custom data types, reuse functions with different data, and create relationships between tables. This flexibility eliminates the need to manage these complexities in programs separately, making PostgreSQL a powerful tool for data management.

ACID compliance: PostgreSQL guarantees reliable data changes since 2001. Every transaction automatically follows the ACID principles, preventing errors and keeping your data trustworthy. ACID stands for Atomicity (all or nothing), Consistency (maintains data rules), Isolation (transactions don't interfere), and Durability (changes are permanent).

Scalability: PostgreSQL seamlessly handles increasing data and complex queries, scaling up or out (adding more servers) to meet the needs of businesses and high-traffic applications. It even allows data to be split across servers for optimal performance.

Advanced features: PostgreSQL goes beyond basics with features like storing JSON and XML data directly, built-in search, automatic data backup and redundancy, customisation options for data types, functions, and operators, and ensuring data consistency through foreign keys.

### Drawbacks

Database development experience: PostgreSQL might feel overwhelming at first for those new to databases due to itsintricate setup and troubleshooting process. MySQL, on the other hand, is a gentler introduction with a smoother learningcurve and easier setup, especially when combined with common web development tools like LAMP.

Overhead: Each new connection in PostgreSQL can potentially consume up to 1.3MB of memory. In productionenvironments with numerous concurrent connections, especially in scalable cloud setups, this can rapidly deplete memoryresources or lead to increased costs.

Admin overhead: Providing high availability (HA) and optimal performance in PostgreSQL can be challenging due to itscomplex configuration and maintenance requirements. The need for additional extensions and components not included in the base distribution adds to this complexity. Managing these components requires expertise, as each has its own releasecycle and upgrade needs.

## Features, purpose and functionalities of the object-relational system (ORM) used in this app

The ORM used in this app is SQLAlchemy.

### Features

Declarative mapping: Defines database tables as Python classes, promoting code readability and maintainability.

Relationships: Easily establishes complex relationships between tables (one-to-one, one-to-many, many-to-many) using Python attributes.

Querying: Constructs intricate SQL queries using Pythonic syntax without raw SQL, providing flexibility and efficiency.

Data modification: Performs CRUD operations on data through Python objects, with SQLAlchemy handling underlying SQL transactions.

Database independence: Creates adaptable code compatible with various databases (PostgreSQL, MySQL, SQLite, etc.). In this app's case it used PostgreSQL as the database system.

Performance optimisation: Enhances performance through features like eager and lazy loading, and query caching.

Advanced features: Supports complex database structures including inheritance, composite keys, custom types, and more.

### Purpose

SQLAlchemy is a powerful Python library that bridges the gap between object-oriented programming and relational databases. Acting as an ORM (Object-Relational Mapper), it translates data between these two paradigms. This allows you to interact with database tables as if they were Python objects, making database operations more intuitive and efficient. 

### Functionalities

Model definition: Create Python classes that represent database tables, defining columns, relationships, and other attributes.

Relationship handling: Manage relationships between objects and automatically synchronise changes.

```py
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    club = db.relationship("Club", back_populates="user", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")
```

Querying: Retrieve data from the database using various query methods and filtering options.

```py
@user_bp.route("/", methods=["GET"])
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)

    return users_schema.dump(users)
```

Data modification: Insert, update, and delete objects, with SQLAlchemy handling the corresponding SQL statements.

Error handling: Provide mechanisms for handling database exceptions and errors.

```py
@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body_data = UserSchema().load(request.get_json())

        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )

        password=body_data.get("password")

        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} field is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "The email address is already registered"}, 409
```

## Entity relationship diagram (ERD) for this app's database, and how the relations between the diagrammed models will aid the database design

![ERD](/docs/erd.png)

The ERD represents the five relational models for my Flask application.

### Users

Attributes

* id: Integer, primary key, unique identifier
* name: String, not null, user's name
* email: String, not null, unqiue, user's email
* password: String, not null, user's password to login
* is_admin: Boolean, default is false, admin status check for authorisation

Relations

* One user MAY create ZERO or ONE book club.

* One user MAY write ZERO or MORE reviews.

### Book Clubs

Attributes

* id: Integer, primary key, unqiue identifier
* name: String, not null, book club's name
* description: String, book club description
* updated: Date, last updated
* user_id: Integer, foreign key, not null, reference to Users

Relations

* One book club MUST BE created by ONE and ONLY ONE user.

* One book club MAY pick ZERO or MANY books (from Book Club Books).

### Books

Attributes

* id: Integer, primary key, unique identifier
* title: String, not null, book's title
* author: String, not null, book's author
* genre: String, not null, book's genre
* summary: String, not null, book summary

Relations

* One book MAY BE picked by ZERO or MANY book clubs (from Book Club Books).

* One book MAY have ZERO or MANY reviews.

### Book Club Books

Attributes

* id: Integer, primary key, unique identifier
* club_id: Integer, foreign key, not null, reference to Book Clubs
* book_id: Integer, foreign key, not null, reference to Books

Relations

* Join table for book club and books tables

### Reviews

Attributes

* id: Integer, primary key, unique identifier
* rating: Integer, not null, user's rating of book
* comment: String, user's comment on book
* user_id: Integer, foreign key, not null, reference to Users
* book_id: Integer, foreign key, not null, reference to Books

Relations

* One review MUST BE written by ONE and ONLY ONE user.

* One review MUST BE assigned to ONE and ONLY one book.

This ERD was revised during coding as I re-evaluated the relationships between the Book Clubs and Books tables. The ERD below is the idea I submitted for approval which shows Books having a many-to-one relationship with Book Clubs whereas I wanted to show that the same book can be picked by many clubs. This meant that the relationship became many-to-many and I needed a join table (Book Club Books).

![First ERD](/docs/1st-erd.png)

## Implemented models and their relationships, including how the relationships aid the database implementation

### User model

```py
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    club = db.relationship("Club", back_populates="user", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")
```

The User model defines the Users table in the relational database.

It has relationships with the Club and Review models using its unique identifier (user_id) as a foreign key to link it to the book club it owns within the Club model and to the reviews its written within Review model. When a user is deleted, the corresponding book club and reviews are deleted too.

### Club model

```py
class Club(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    updated = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="club")
    club_books = db.relationship("ClubBook", back_populates="club", cascade="all, delete")
```

The Club model defines the Book Clubs table in the relational database.

It has relationships with the User and Club Book model. The unique identifier of the User model (user_id) is a foreign key within the Club model. The Club model uses its unique identifier (club_id) as a foreign key to link it to the Books model via the Club Book join model. When a book club is deleted, the corresponding books are deleted from the book club but not from the database.

### Book model

```py
class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)

    club_books = db.relationship("ClubBook", back_populates="book", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete")
```

The Book model defines the Books table in the relational database.

It has relationships with Club Book and Review models using its unique identifier (book_id) as a foreign key to link it to the book clubs it's in via the Club Book join model and to the reviews it has within the Review model. When a book is deleted, the corresponding book club assignment and reviews are deleted too.

### Club Book model

```py
class ClubBook(db.Model):
    __tablename__ = "club_books"

    id = db.Column(db.Integer, primary_key=True)

    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    club = db.relationship("Club", back_populates="club_books")
    book = db.relationship("Book", back_populates="club_books")
```

The Club Book model defines the Book Club Books table in the relational database.

It has relationships with the Club and Book model as it is the join model for them. The unique identifier of the Club and Book models (club_id and book_id) are foreign keys within the Club Book model.

### Review model

```py
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    book = db.relationship("Book", back_populates="reviews")
```

The Review model defines the Reviews table in the relational database.

It has relationships with the User and Book models. The unique identifier of the User and Books models (user_id and book_id) are foreign keys within the Review model.

## How to use this application's API endpoints

1. Open your terminal of choice and navigate to the directory you'd like to clone the repository to.

2. Clone the GitHub repository via SSH:

```sh
git clone git@github.com:kimnle/T2A2-APIWebServer.git
```

Or HTTPS:

```sh
git clone https://github.com/kimnle/T2A2-APIWebServer.git
```

3. Navigate to the "src" folder in the cloned repository:

```sh
cd T2A2-APIWebServer/src
```

4. Create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

5. Install the requirements for the API within the virtual environment:

```sh
pip3 install -r requirements.txt
```

6. Start PostgreSQL:

```sh
sudo -u postgres psql
```

7. Create a database and a database user and give the user permission within PostgreSQL:

```sql
CREATE DATABASE club_db;
CREATE USER club_dev WITH PASSWORD "your_password";
GRANT ALL PRIVILEGES ON DATABASE club_db TO club_dev;
```

8. Create a ".env" file and place the variables from ".envsample" into this file adding your own ```DATABASE_URL``` and ```JWT_SECRET_KEY```:

```sh
DATABASE_URL="postgresql+psycopg2://club_dev:your_password@localhost:5432/club_db"
JWT_SECRET_KEY="your_jwt_secret_key"
```

9. Create and seed tables using commands:

```sh
flask db create
flask db seed
```

10. Run the server:

```sh
flask run
```

### User routes

GET - /user

* Gets all user records from the database

* No required body or header data

* Response: List of all registered users in the database, displaying ID, name, email, admin status, book club (if any), and reviews (if any).

![GET /user](/docs/get-userr.png)

GET - /user/int:user_id

* Gets a single user record from the database

* Header: user_id is required

* Response: Corresponding registered user in the database, displaying ID, name, email, admin status, book club (if any), and reviews (if any)

![GET /user/id](/docs/get-user-id.png)

Or an error

![GET /user/id 404](/docs/get-user-id-404.png)

POST - /user/register

* Creates a new user record in the database

* Body requires:

    * Name: Alphabet characters only

    * Email

    * Password: Minimum eight characters with at least one uppercase letter, one lowercase letter, one number and one special character

* Response: The newly registered user's ID, name, email, admin status, empty book club field, and empty reviews field

![POST /user/register](/docs/post-user-register.png)

Or errors

![POST /user/register 409](/docs/post-user-register-409.png)

![POST /user/register 409b](/docs/post-user-register-409b.png)

POST - /user/login

* Logs in user

* Body requires: Email and password

* Response: The logged in user's email, admin status and JWT token

![POST /user/login](/docs/post-user-login.png)

Or an error

![POST /user/login 401](/docs/post-user-login-401.png)

DELETE - /user/int:user_id

* Deletes a user record from the database by either the user themselves or a user with admin privileges (valid JWT token required)

* Header: user_id required

* Response: A message

![DELETE /user/id](/docs/delete-user-id.png)

Or errors

![DELETE /user/id 403](/docs/delete-user-id-403.png)

![DELETE /user/id 404](/docs/delete-user-id-404.png)

PUT, PATCH - /user/int:user_id

* Updates a user record in the database by the user themselves (valid JWT token required)

* Header: user_id required

* Body requires: Updated name, email and/or password

* Response: The newly updated user's ID, name, email, admin status, book club (if any), and reviews (if any)

![PUT, PATCH /user/id](/docs/put-user-id.png)

Or errors

![PUT, PATCH /user/id 403](/docs/put-user-id-403.png)

![PUT, PATCH /user/id 404](/docs/put-user-id-404.png)

### Club routes

GET - /club

* Gets all book club records from the database

* No required body or header data

* Response: List of all registered book clubs in the database, displaying ID, name, description, last updated date, owner, and book picks (if any)

![GET /club](/docs/get-club.png)

GET - /club/int:club_id

* Gets a single book club record from the database

* Header: club_id is required

* Response: Corresponding registered book club in the database, displaying ID, name, description, last updated date, owner, and book picks (if any)

![GET /club/id](/docs/get-club-id.png)

Or an error

![GET /club/id 404](/docs/get-club-id-404.png)

POST - /club

* Creates a new book club record in the database by the logged in user (valid JWT token required)

* Body requires: Name and/or optional description

* Response: The newly registered book clubs's ID, name, description (if any), updated date of today, logged in user as owner, and empty book picks field

![POST /club](/docs/post-club.png)

DELETE - /club/int:club_id

* Deletes a book club record from the database by either the user who owns the book club or a user with admin privileges (valid JWT token required)

* Header: club_id required

* Response: A message

![DELETE /club/id](/docs/delete-club-id.png)

Or errors

![DELETE /club/id 403](/docs/delete-club-id-403.png)

![DELETE /club/id 404](/docs/delete-club-id-404.png)

PUT, PATCH - /club/int:club_id

* Updates a book club record in the database by the user who owns the book club (valid JWT token required)

* Header: user_id required

* Body requires: Updated name and/or description

* Response: The newly updated book club's ID, name, description (if any), updated date of today, owner, and book picks (if any)

![PUT, PATCH /club/id](/docs/put-club-id.png)

Or errors

![PUT, PATCH /club/id 403](/docs/put-club-id-403.png)

![PUT, PATCH /club/id 404](/docs/put-club-id-404.png)

### Book routes

GET - /book

* Gets all book records from the database

* No required body or header data

* Response: List of all books in the database, displaying ID, title, author, genre, summary, book clubs that have picked it (if any), and reviews (if any)

![GET /book](/docs/get-book.png)

GET - /book/int:book_id

* Gets a single book record from the database

* Header: book_id is required

* Response: Corresponding book in the database, displaying ID, title, author, genre, summary, book clubs that have picked it (if any), and reviews (if any)

![GET /book/id](/docs/get-book-id.png)

Or an error

![GET /book/id 404](/docs/get-book-id-404.png)

POST - /book

* Creates a new book record in the database

* Body requires:

    * Title

    * Author: Alphabet characters only

    * Genre: Fiction or Non-fiction

    * Summary

* Response: The newly created clubs's ID, title, author, genre, summary, empty book clubs field, and empty reviews field

![POST /book](/docs/post-book.png)

DELETE - /book/int:book_id

* Deletes a book record from the database by a user with admin privileges (valid JWT token required)

* Header: book_id required

* Response: A message

![DELETE /book/id](/docs/delete-book-id.png)

Or errors

![DELETE /book/id 403](/docs/delete-book-id-403.png)

![DELETE /book/id 404](/docs/delete-book-id-404.png)

PUT, PATCH - /book/int:book_id

* Updates a book record in the database by a user with admin privileges (valid JWT token required)

* Header: book_id required

* Body requires: Updated title, author, genre and/or summary

* Response: The newly updated book's ID, title, author, genre, summary, book clubs that have picked it (if any), and reviews (if any)

![PUT, PATCH /book/id](/docs/put-book-id.png)

Or errors

![PUT, PATCH /book/id 403](/docs/put-book-id-403.png)

![PUT, PATCH /book/id 404](/docs/put-book-id-404.png)

POST - /book/int:book_id/club/int:club_id

* Creates an assignment record in the database of a book to a book club by the user who owns the book club (valid JWT token required)

* Header: book_id and club_id required

* Response: The assignment's ID, and the assigned book club and book

![POST /book/id/club/id](/docs/post-book-id-club-id.png)

Or errors

![POST /book/id/club/id 403](/docs/post-book-id-club-id-403.png)

![POST /book/id/club/id 404](/docs/post-book-id-club-id-404.png)

DELETE - /book/int:book_id/club/int:club_id

* Deletes an assignment record from the database of a book from a book club by the user who owns the book club (valid JWT token required)

* Header: book_id and club_id required

* Response: A message

![DELETE /book/id/club/id](/docs/delete-book-id-club-id.png)

Or errors

![DELETE /book/id/club/id 403](/docs/delete-book-id-club-id-403.png)

![DELETE /book/id/club/id 404](/docs/delete-book-id-club-id-404.png)

### Review routes

POST - /book/int:book_id/review

* Creates a new review record in the database to a book

* Header: book_id required

* Body requires:

    * Rating: One to five

    * Comment (optional)

* Response: The newly created review's ID, rating, comment (if any), owner, book, and book clubs that have picked it (if any)

![POST /book/id/review](/docs/post-book-id-review.png)

Or an error

![POST /book/id/review 404](/docs/post-book-id-review-404.png)

DELETE - /book/int:book_id/review/int:review_id

DELETE - /book/int:book_id

* Deletes a review record from the database from a book by either the user who owns the book club or a user with admin privileges (valid JWT token required)

* Header: book_id and review_id required

* Response: A message

![DELETE /book/id/review/id](/docs/delete-book-id-review-id.png)

Or errors

![DELETE /book/id/review/id 403](/docs/delete-book-id-review-id-403.png)

![DELETE /book/id/review/id 404](/docs/delete-book-id-review-id-404.png)