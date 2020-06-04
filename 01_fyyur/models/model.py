from typing import Any, Dict, List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Model():
    """This is the base class for database models."""

    __abstract__: bool = True

    def insert(self):
        """Inserts a row into the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, **attributes):
        """Updates a row in the database."""
        for key, value in attributes.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """Deletes a row from the database."""
        db.session.delete(self)
        db.session.commit()


db = SQLAlchemy(model_class=Model)
