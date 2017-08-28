from flask import Flask

from app.vectorize import tokenize
import __main__

setattr(__main__,'tokenize',tokenize)

app = Flask(__name__)
app.config.from_object('config')


from app import views

