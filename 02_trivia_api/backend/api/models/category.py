"""Defines the trivia Category model."""
from typing import Any, Dict, Optional

from api.models.model import db, Model


class Category(Model):
    """This class represents a trivia Category."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type = db.Column(db.String)

#    def __init__(self, question, answer, category, difficulty):
#        self.question = question
#        self.answer = answer
#        self.category = category
#        self.difficulty = difficulty

    @classmethod
    def validate_all(cls, json: Dict[str, Any]) -> None:
        """Validates all model attributes of this resource."""
        pass
