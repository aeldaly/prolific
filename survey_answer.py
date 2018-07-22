import functools

from flask import (
  Blueprint,
  jsonify,
  request
)

import sqlite3

from prolific.db import get_db

bp = Blueprint('survey_answer', __name__, url_prefix='/survey_answers')

@bp.route('', methods=['GET'])
def index():
  survey_answers = get_db().execute('SELECT * FROM survey_responses').fetchall()

  if survey_answers:
    return jsonify(survey_answers)
  else:
    return 'No Survey Answers in System'


@bp.route('', methods=['POST'])
def create():
  survey_id = request.form['survey']
  user_id = request.form['user']

  db = get_db()

  survey = db.execute(
      'SELECT * FROM surveys WHERE id = ?', survey_id
  ).fetchone()

  if survey:
    survey_answers_count = survey['survey_answers_count']
    available_places = survey['available_places']

    if survey_answers_count < available_places:
      try:
        db.execute(
          'INSERT INTO survey_responses (survey, user) VALUES (?, ?)',
          (survey_id, user_id)
        )
        db.execute(
            'UPDATE surveys SET survey_answers_count = ? WHERE id = ?',
            (survey_answers_count + 1, survey_id)
        )
        db.commit()

        return 'Successfully created Survey Answer'
      except sqlite3.IntegrityError:
        return 'User has already submitted response for this survey', 400
    else:
      return 'Maximum responses for this survey reached', 400
  else:
    return 'This Survey does not exist in the system', 400
