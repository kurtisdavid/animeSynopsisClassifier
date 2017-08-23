#!flask/bin/python
from app import app
from app.vectorize import tokenize
app.run(debug=True)