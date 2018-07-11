import functools

from flask import (
  Blueprint,
  jsonify,
  request
)

from prolific.db import get_db

bp = Blueprint('survey_answer', __name__, url_prefix='/survey_answers')

@bp.route('', methods=['GET'])
def index():
  survey_answers = get_db().execute('SELECT * FROM survey_answers').fetchall()
  return jsonify(survey_answers)


@bp.route('', methods=['POST'])
def create():
  survey = request.form['survey']
  user = request.form['user']

  db = get_db()
  db.execute(
    'INSERT INTO survey_answers (survey, user) VALUES (?, ?)',
    (survey, user)
  )
  db.commit()

  return 'SUCCESSFULLY CREATED SURVEY ANSWER'