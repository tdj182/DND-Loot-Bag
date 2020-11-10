"""SQLAlchemy models for Warbler."""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    lootbags = db.relationship(
        "Lootbag", cascade="all,delete", backref="user")

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Lootbag(db.Model):
    """A unique lootbag"""

    __tablename__ = 'lootbags'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        default="No name"
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    is_shareable = db.Column(db.Boolean, nullable=False, default=False)

    platinum = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    gold = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    electrum = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    silver = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    copper = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    items = db.relationship(
        'Item', secondary="lootbags_items", cascade="all,delete", backref="lootbag")


class LootbagItem(db.Model):
    """Item in Lootbag"""

    __tablename__ = 'lootbags_items'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    lootbag_id = db.Column(
        db.Integer,
        db.ForeignKey('lootbags.id', ondelete='cascade'),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey('items.id', ondelete='cascade'),
        nullable=False
    )


class Item(db.Model):
    """All items created."""

    __tablename__ = 'items'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    item_name = db.Column(
        db.Text,
        nullable=False,
        default="No Name"
    )

    rarity = db.Column(
        db.Text
    )

    text = db.Column(
        db.Text
    )

    requires_attunement = db.Column(
        db.Text
    )

    slug = db.Column(
        db.Text
    )

    type = db.Column(
        db.Text
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
