import functools
import sqlite3

from flask import (
  Blueprint,
  jsonify,
  request
)

from prolific.db import get_db

bp = Blueprint('survey', __name__, url_prefix='/surveys')

@bp.route('', methods=['GET'])
def index():
  surveys = get_db().execute('SELECT * FROM surveys').fetchall()

  if surveys:
    return jsonify(surveys)

  return 'No Surveys in System'


@bp.route('', methods=['POST'])
def create():
  name = request.form['name']
  available_places = request.form['available_places']
  user = request.form['user']

  db = get_db()

  try:
    db.execute(
      'INSERT INTO surveys (name, available_places, user) VALUES (?, ?, ?)',
      (name, available_places, user)
    )
    db.commit()
  except sqlite3.IntegrityError:
    return 'Survey with this name already exists', 400

  return 'SUCCESSFULLY CREATED SURVEY'
