"""Defines the trivia Question model."""
from typing import Any, Dict, Optional

from api.models.model import db, Model


class Question(Model):
    """This class represents a trivia Question."""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    category = db.Column(db.String)
    difficulty = db.Column(db.Integer)

#    def __init__(self, question, answer, category, difficulty):
#        self.question = question
#        self.answer = answer
#        self.category = category
#        self.difficulty = difficulty

    @classmethod
    def validate_all(cls, json: Dict[str, Any]) -> None:
        """Validates all model attributes of this resource."""
        pass
