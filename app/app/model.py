import pickle
import gzip
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC


def get_svm():

    # load trained SVM
    with gzip.open('../models/svc_p.zip', 'rb') as f:
        clf = pickle.load(f)

    return clf

def get_ranks():

    with open('../models/ranking_dict.pkl', 'rb') as f:
    
        ranking_dict = pickle.load(f)

    return ranking_dict

def get_genres():

    with open('../models/genres.pkl', 'rb') as f:
    
        genres = pickle.load(f)

    return genres

def predict(pipeline, synopsis, genres, true_genres, ranking_dict):

    # predicted labels
    predicted = pipeline.predict([synopsis])[0]
    # corresponding probabilities
    proba_ = pipeline.predict_proba([synopsis])[0]

    # labels converted to genre names
    predictions = list(np.asarray(genres)[predicted==1])

    # binary labels of true genres
    true_binary = np.zeros(43)
    true_binary[[genres.index(g) for g in true_genres]] = 1

    # numpy mask of sum of binary labels; nonzero elements will be the union of all positives
    combined = np.nonzero(true_binary + predicted)

    # numpy mask of difference of labels; negative elements will be all true genres NOT predicted positive by the model
    incorrect = np.where(predicted-true_binary<0)[0]

    mean = (np.sum(proba_[predicted==1]) + np.sum(1-proba_[incorrect]))/combined[0].size

    '''
    Now get top 10 descriptors for each predicted label
    '''

    vectorizer = pipeline.named_steps['vect']
    n_grams = vectorizer.inverse_transform(vectorizer.transform([synopsis]))[0]

    top_descriptors = {}

    for genre in predictions:

        ranks = {}

        for n_gram in n_grams:

            if n_gram in ranking_dict:

                ranks[n_gram] = ranking_dict[n_gram][genres.index(genre)]

        sorted_ = sorted(ranks, key=ranks.get, reverse=True)

        top_descriptors[genre] = [k for k in sorted_[:min(10, len(sorted_))]]

    return predictions, mean, top_descriptors