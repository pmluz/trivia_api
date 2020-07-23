import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        # print('Categories:', categories)  # test to check

        return jsonify({'success': True, 'categories': categories})

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            categories = {}
            for category in Category.query.all():
                categories[category.id] = category.type

            if len(selection) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': categories
            })

        except Exception:
            abort(404)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(422)

            question.delete()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question.id,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except ValueError:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')

        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                difficulty=new_difficulty,
                                category=new_category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            # current_questions = paginate_books(request, selection)
            return jsonify({
                'success': True,
                'question': question.format(),
                'created': question.id,
                'total_questions': len(selection)
            })
        except ValueError:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm')

            search_query = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            search_results = paginate_questions(request, search_query)

            if (len(search_query) == 0):
                abort(404)

            return jsonify({
                'success': True,
                'questions': search_results,
                'total_questions': len(search_query)
            })
        except Exception:
            abort(404)

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_by_categories(id):
        try:
            selection = Question.query.filter(Question.category == id).all()
            current_questions = paginate_questions(request, selection)

            category = Category.query.filter(Category.id == id).one_or_none()

            if category is None:
                abort(422)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': str(category.type)
            })

        except ValueError:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()

            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            # category = all
            if quiz_category['id'] == 0:
                selection = Question.query.all()
            # specific category
            else:
                selection = Question.query.filter_by(
                    category=quiz_category['id']).all()

            total_length = len(selection)

            for i in range(total_length):
                random_question = random.choice(selection)
                if random_question.id not in previous_questions:
                    question = random_question.format()
                else:
                    random_question = random.choice(selection)

            # loops upto all questions in categories < 5
            if len(previous_questions) == total_length:
                return jsonify({'success': True})

            return jsonify({
                'success': True,
                'previousQuestion': previous_questions,
                'totalQuestions': len(selection),
                'question': question
            })

        except SyntaxError:
            abort(400)

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    return app
