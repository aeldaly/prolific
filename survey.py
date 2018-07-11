import functools

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
  return jsonify(surveys)


@bp.route('', methods=['POST'])
def create():
  name = request.form['name']
  available_places = request.form['available_places']
  user = request.form['user']

  db = get_db()
  db.execute(
    'INSERT INTO surveys (name, available_places, user) VALUES (?, ?, ?)',
    (name, available_places, user)
  )
  db.commit()

  return 'SUCCESSFULLY CREATED SURVEY'