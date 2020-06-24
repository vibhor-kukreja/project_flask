from app.auth.models import Base
from app import db


class Followers(Base):
    # TODO: To implement this to save friends/rooms a user is in
    __tablename__ = "followers"

    mail = db.Column(db.String(128), nullable=False)
    friend = db.Column(db.String(128), nullable=True)
    room = db.Column(db.String(128), nullable=True)
