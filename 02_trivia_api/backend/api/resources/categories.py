"""API interface for authors."""
import datetime

from flask import Response, jsonify, request
from typing import Optional

from api.models.category import Category
from api.models.question import Question
from api.exception import BadRequestException
from api.resources.resource import Resource, register_api_all


class CategoryAPI(Resource):
    """Class representing the author interface into the API."""

    def get(self, resource_id: int) -> Response:
        """Fetches a category of questions from the database."""
        questions = Question.fetch_all_filtered({'category': resource_id})
        question_count = Question.count_all()
        category = Category.fetch_by_id(resource_id)
        #questions
        #total_questions
        #current_category

        response = {
            'success': True,
            'questions': questions,
            'total_questions': question_count,
            'current_category': category,
        }

        #return jsonify(category)
        #return jsonify(questions)
        return jsonify(response)


register_api_all(view=CategoryAPI, endpoint='category_api', model=Category, url='/categories')
