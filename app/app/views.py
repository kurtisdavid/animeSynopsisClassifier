from flask import render_template, flash, redirect, request, url_for, make_response
from app import app
from .forms import LoginForm
from .scrape import scrape, clean, generate
from .vectorize import tokenize,get_vectorizer
from .model import get_svm, predict, get_ranks, get_genres
from sklearn.pipeline import Pipeline
import json
import urllib.request
from bs4 import BeautifulSoup
import random

vectorizer = None
clf = None
pipeline = None
genres = None
ranking_dict = None


start = False

@app.route('/', methods = ['GET', 'POST'])
def login():

    global start
    global vectorizer
    global clf
    global pipeline
    global genres
    global ranking_dict

    if not start:

        init_models()
        start = True

    form = LoginForm()

    if form.validate_on_submit():

    	return redirect('/classify', form.openid.data)

    return render_template('index.html',
                           title='Sign In',
                           form=form, error = None)

@app.route('/classify',  methods = ['GET', 'POST'])

def classify():

    global vectorizer
    global clf
    global pipeline
    global genres
    global ranking_dict

    form = LoginForm()

    if request.method == 'POST':

        results = scrape(request.form['anime_link'])

        if results == None:

            return render_template('index.html',
                           title='Sign In',
                           form=form, error = "Please use a valid link.")

        elif results == 0:

            return render_template('index.html',
                           title='Sign In',
                           form=form, error = "Could not find a valid synopsis.")

        title, (synopsis, true_genres), img = results[0], results[1], results[2]

        if clf==None or vectorizer==None or pipeline==None or genres==None or ranking_dict==None:
            init_models()

        predictions, mean, top_descriptors = predict(pipeline,synopsis,genres, true_genres, ranking_dict)

        confidence = str(int(mean*100)) + '%'

        return render_template('classify.html', title='Home', name = title.replace('_',' '), predictions = predictions, mean = json.dumps(mean),
            confidence = confidence, form = form, img_link = img, synopsis = synopsis, top_10 = top_descriptors)

    if form.validate_on_submit():
        return redirect('/classify', form.openid.data)

@app.route('/generate', methods =['GET','POST'])

def generate():

  general_link = "https://myanimelist.net/anime/season"
  r = urllib.request.urlopen(general_link).read()
  soup = BeautifulSoup(r,'lxml')

  seasonal_anime = soup.findAll('div', class_ = 'seasonal-anime js-seasonal-anime');
  chosen = random.choice(seasonal_anime)

  link = chosen.div.div.p.a.get('href')

  return link

def init_models():

    global start
    global vectorizer
    global clf
    global pipeline
    global genres
    global ranking_dict

    vectorizer = get_vectorizer()
    clf = get_svm()
    ranking_dict = get_ranks()
    genres = get_genres()
    pipeline = Pipeline([ ('vect', vectorizer), ('clf', clf) ])
