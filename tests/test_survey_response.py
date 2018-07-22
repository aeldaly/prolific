import pytest
import json

from ..db import get_db


def test_get_survey_responses_empty_db(client):
    response = client.get('/survey_responses')

    assert response.status_code == 200
    assert response.data == b'No Survey Responses in System'


def test_get_surveys(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            'INSERT INTO survey_responses (survey, user) VALUES (?, ?)',
            (1, 11)
        )

        response = client.get('/survey_responses')
        json_response = json.loads(response.get_data(as_text=True))[0]

        assert response.status_code == 200
        assert json_response['survey'] == 1
        assert json_response['user'] == 11


def test_create_survey_response_with_no_survey(client, app):
    response = client.post(
        '/survey_responses', data={
            'survey': '1',
            'user': 77
        }
    )

    assert response.status_code == 400
    assert response.data == b'This Survey does not exist in the system'


def test_create_survey_response(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            'INSERT INTO surveys (name, user) VALUES (?, ?)',
            ('Survey 1', 11)
        )

        response = client.post(
            '/survey_responses', data={
                'survey': 1,
                'user': 77
            }
        )

        assert response.status_code == 200
        assert response.data == b'Successfully created Survey Response'

        row = get_db().execute(
            'SELECT * FROM surveys'
        ).fetchall()[0]

        assert row['survey_responses_count'] == 1
        

def test_create_survey_response_max_reached(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            'INSERT INTO surveys (name, user, available_places) VALUES (?, ?, ?)',
            ('Survey 1', 11, 1)
        )

        client.post(
            '/survey_responses', data={
                'survey': 1,
                'user': 77
            }
        )
        
        response = client.post(
            '/survey_responses', data={
                'survey': 1,
                'user': 78
            }
        )

        assert response.status_code == 400
        assert response.data == b'Maximum responses for this survey reached'

        row = get_db().execute(
            'SELECT * FROM surveys'
        ).fetchall()[0]

        assert row['survey_responses_count'] == 1


def test_create_survey_response_duplicate_user(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            'INSERT INTO surveys (name, user) VALUES (?, ?)',
            ('Survey 1', 11)
        )

        client.post(
            '/survey_responses', data={
                'survey': 1,
                'user': 77
            }
        )

        response = client.post(
            '/survey_responses', data={
                'survey': 1,
                'user': 77
            }
        )

        assert response.status_code == 400
        assert response.data == b'User has already submitted response for this survey'

        row = get_db().execute(
            'SELECT * FROM surveys'
        ).fetchall()[0]

        assert row['survey_responses_count'] == 1
