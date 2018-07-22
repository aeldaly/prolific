import pytest
import json

from ..db import get_db


def test_get_surveys_empty_db(client):
    response = client.get('/surveys')

    assert response.status_code == 200
    assert response.data == b'No Surveys in System'


def test_get_surveys(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            'INSERT INTO surveys (name, user) VALUES (?, ?)',
            ('RHCP', 11)
        )

        response = client.get('/surveys')

        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True))[0] == {
            'available_places': 30,
            'id': 1,
            'name': 'RHCP',
            'survey_responses_count': 0,
            'user': 11
        }

def test_create_survey(client, app):
    client.post(
        '/surveys', data={
            'name': 'name of survey',
            'available_places': 45,
            'user': 77
        }
    )

    with app.app_context():
        row = get_db().execute(
            'SELECT * FROM surveys'
        ).fetchall()[0]

        assert row == {
            'id': 1,
            'name': 'name of survey',
            'available_places': 45,
            'survey_responses_count': 0,
            'user': 77
        }


def test_create_survey_duplicate_key(client, app):
    client.post(
        '/surveys', data={
            'name': 'name of survey',
            'available_places': 45,
            'user': 77
        }
    )

    response = client.post(
        '/surveys', data={
            'name': 'name of survey',
            'available_places': 45,
            'user': 79
        }
    )

    assert response.status_code == 400
    assert response.data == b'Survey with this name already exists'
