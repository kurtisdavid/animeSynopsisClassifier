import re
import nltk
import pickle
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

def tokenize(text):
    
    regex = re.compile('[^ \w]', re.U)

    text = regex.sub(' ', text).lower()
    
    tokens = np.asarray(nltk.word_tokenize(text))
    
    valid = [s not in ENGLISH_STOP_WORDS for s in tokens]
    
    tokens = tokens[valid]
    
    lemm = []
    
    lemmatizer = WordNetLemmatizer()
    
    for token in tokens:
        
        lemm.append(lemmatizer.lemmatize(token))
    
    return lemm

def get_vectorizer():

    # load trained tfidf vectorizer 
    with open('../models/vect.pkl','rb') as f:
        vectorizer = pickle.load(f)

    return vectorizer