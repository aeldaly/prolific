# Installation
1. `pip3 install virtualenv`
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `FLASK_APP=. FLASK_ENV=development flask init-db`
6. `FLASK_APP=. FLASK_ENV=development flask run`

The server will now be up and running on port 5000

# API

* GET /surveys -- list all surveys
* POST /surveys -- create a new survey. Parameters are survey name `name`, user_id `user` , and available spots `available_places`
  * eg: `curl --data "name=Survey2d1&available_places=1&user=1" http://localhost:5000/surveys`

* GET /survey_responses -- list all survey responses
* POST /survey_responses -- create a new survey response. Paramaters are survey_id `survey`, user_id `user`
  * eg: curl --data "survey=2&user=33" http://localhost:5000/survey_responses

# TESTS
run tests by running `pytest` from the root of the codebase

# Design Considerations
1. For expediency, using sqlite3 as the database. It comes standard with Python and doesn't require much configuration. In production an RDBMS (postgresql) or a NoSql DB (Mongo) would be used.
