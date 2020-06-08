"""API interface for trivia questions."""
#from typing import Optional, Tuple

from flask import Response, abort, jsonify, request
#from flask.views import MethodView
from sqlalchemy import exists
#from sqlalchemy import exc, exists
from typing import Optional


#from api.app import app
from api.exception import BadRequestException
from api.models.category import Category
from api.models.question import Question
from api.models.model import db
from api.resources.resource import Resource, register_api_all
from config import Config


class QuestionAPI(Resource):
    """Class representing the Question interface into the API."""

    def get(self, resource_id: Optional[int] = None) -> Response:
        """Fetches one or more questions from the database.
        If 'resource_id' is given, return that specific question,
        else if the 'page' HTTP parameter is set, return than page of questions,
        else return all questions."""
        if resource_id is not None:
            questions = [Question.fetch_by_id(resource_id)]
        elif 'page' in request.args:
            page = int(request.args.get('page'))
            questions = Question.fetch_page(page, Config.PAGE_LENGTH)
        else:
            questions = Question.fetch_all(Question.id)

        question_count = Question.count_all()

        categories = list(set([
            Category.fetch_by_id(question['category'])['type']
            for question
            in questions
        ]))

        if len(questions) == 1:
            current_category = categories[0]
        else:
            current_category = None

        response = {
            'success': True,
            'questions': questions,
            'totalQuestions': question_count,
            'categories': categories,
            'currentCategory': current_category,
        }

        return jsonify(response)


register_api_all(view=QuestionAPI, endpoint='question_api', model=Question, url='/questions')
