# Installation
1. run `pip3 install virtualenv`
2. run `virtualenv . venv/bin/activate`
3. run `pip install -r requirements.txt`

# Design Considerations
1. For expediency, using sqlite3 as the database. It comes standard with Python and doesn't require much configuration. In production an RDBMS (postgresql) or a NoSql DB (Mongo) would be used.
