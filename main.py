import os

from flask import Flask

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from controllers.club_controller import club_bp
    app.register_blueprint(club_bp)

    return app