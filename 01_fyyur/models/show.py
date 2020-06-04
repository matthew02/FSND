from models.model import db, Model


class Show(Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_time = db.Column(db.DateTime)
    venue_id = db.Column(
        db.Integer,
        db.ForeignKey('venue.id', ondelete='cascade'),
        nullable=False
    )
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('artist.id', ondelete='cascade'),
        nullable=False
    )

    def __repr__(self):
        return f'<Show {self.id} {self.start_time}>'
