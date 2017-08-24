# animeSynopsisClassifier
Multilabel classification of synopses from all the anime listed on MyAnimeList.net

This project has two parts:

# 1. Jupyter Notebook
This is where I spent a lot of exploration on the datasets that focuses on the data science portion of the project.

If you'd like to view the notebook view it here: 
[animeSynopsisClassifier](https://nbviewer.jupyter.org/github/kurtisdavid/animeSynopsisClassifier/blob/master/AnimeSynopsisClassifier.ipynb)

The final result had an **F-score** of 0.81 over 43 labels. 

This final model used a **linear Support Vector Machine** after GridSearch and testing other models: (Logistic Regression, Naive Bayes, Random Forest).

# 2. Flask Web Application
To make my results interactive, I built a python web app using [Flask](http://flask.pocoo.org/). Click here to check it out! (Link coming soon)

Here are some screenshots:

### Main App Page:
![Home](https://github.com/kurtisdavid/animeSynopsisClassifier/blob/master/images/Home.PNG)

The main page has two main parts:
* The first is a manual input of a MyAnimeList.net (MAL) link to one of their anime.
  * ex) [Naruto Shippuden](https://myanimelist.net/anime/1735/Naruto__Shippuuden)
  * Afterwards, by clicking "Classify", the user is sent to a new page which will contain the machine learning model's predictions + some analysis.
* The second is a button that generates a random link from MAL's [current season](https://myanimelist.net/anime/season) page and goes straight to the analysis. This makes it easier to test out the site without having to look up a link.

### Example Prediction on Naruto:
![Naruto1](https://github.com/kurtisdavid/animeSynopsisClassifier/blob/master/images/example1.PNG)

Here is an example of the app in action!

Given the link, it scrapes the information of the anime from the link and submits it into the model. If invalid, an error occurs.

It makes two main calculations:
* The first are the predicted genres of the anime. It uses the anime's synopsis + the name, studio, and rating as meta-data for text-classification.
  * The genres will be shown at the very top under the tile as buttons. By clicking each, the user can see further analysis (picture below)
* The second is a "% confidence" score. I didn't read up on any official metrics, but this is how I calculated mine:
  * Take all of the **positive predictions** the model made. Retrieve their corresponding probabilities and sum up.
  * Take all of the **negative predictions** the model made that were **TRUE LABELS** (i.e. incorrect). Calculate 1-(corresponding probabilities) and sum up.
  * Add the two sums and divide by the size of the **union of positive predictions and true labels**. This is the final confidence score!


### Example Genre Highlights:

![Naruto2](https://github.com/kurtisdavid/animeSynopsisClassifier/blob/master/images/example2.PNG)

By clicking on one of the genre buttons at the top, the app then highlights (with the same color as the button) the **top indicators** for predicting that certain genre. 

It utilizes the linear Support Vector Machine's hyperplane by taking it's components' weights to get the top words+phrases. More explanation can be found in my notebook linked above.

The tool utilizes the jQuery [highlight](http://johannburkard.de/blog/programming/javascript/highlight-javascript-text-higlighting-jquery-plugin.html) library developed by Johann Burkard. 
* I had to make a few changes, primarily fixing bugs that dealt with highlighting words more than once + string matching. All edits are found [here](https://github.com/kurtisdavid/animeSynopsisClassifier/blob/master/app/app/static/js/jquery.highlight-5.js).

### Another Example:

![Toradora](https://github.com/kurtisdavid/animeSynopsisClassifier/blob/master/images/example3.PNG)

A few nice highlights for Romance:
* romantic
* love
* crush
* student (?)

As I played around with the tool, I realized that the model overfit, so if I were to work on the model again, I would decrease the number of word features + increase regularization to help with generalizing.
