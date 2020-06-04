from models.model import db, Model


class Artist(Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship(
        'Show',
        backref='artist',
        cascade='all, delete',
        lazy=True,
    )

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'
