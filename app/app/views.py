from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
from .scrape import scrape, clean
from .vectorize import tokenize, get_vectorizer
from .model import get_svm, get_genres, predict, get_ranks
from sklearn.pipeline import Pipeline
import json


vectorizer = None
clf = None
pipeline = None
genres = None
ranking_dict = None


start = False

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])

def login():

    global start
    global vectorizer
    global clf
    global pipeline
    global genres
    global ranking_dict

    if not start:

        genres = get_genres()
        vectorizer = get_vectorizer()
        clf = get_svm()
        ranking_dict = get_ranks()
        pipeline = Pipeline([ ('vect', vectorizer), ('clf', clf) ])
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


        title, (synopsis, true_genres), img = results[0], results[1], results[2] 

        predictions, mean, top_descriptors = predict(pipeline,synopsis,genres, true_genres, ranking_dict)

        confidence = str(int(mean*100)) + '%'



        return render_template('classify.html', title='Home', name = title.replace('_',' '), predictions = predictions, mean = json.dumps(mean),
            confidence = confidence, form = form, img_link = img, synopsis = synopsis, top_10 = top_descriptors)

    if form.validate_on_submit():
        return redirect('/classify', form.openid.data)