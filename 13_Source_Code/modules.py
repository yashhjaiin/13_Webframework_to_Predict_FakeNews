import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from csv import writer

import os
import re
import nltk
import joblib

from nltk.sentiment.vader import SentimentIntensityAnalyzer

pipeline = joblib.load('./notebook_work/retrainPipeline.sav')

#Feature extraction
def preprocess(title, text):
    val = title+". "+text
    filter_sentence = ''
    lemmatizer = WordNetLemmatizer()

    sentence = re.sub(r'[^\w\s]','', val)                #cleaning using regular expression
    words = nltk.word_tokenize(sentence)                 #Applying tokenization
    for word in words:
        if word.startswith('https'):
            word =  "link"
        filter_sentence = filter_sentence + ' ' + str(lemmatizer.lemmatize(word)).lower()       #Applying lemmatization
    return filter_sentence

def predict(val):
    pred = pipeline.predict_one(val)
    dic = {1:'REAL',0:'NOT REAL'}

    return dic[pred]

# def retrain(result, poll, val):

    

#     return result 

def sentimentPrediction(title):
    sia = SentimentIntensityAnalyzer()
    res = sia.polarity_scores(title)['compound']
    if(res > 0):
        sentiment_res = "Positive"
    elif(res < 0):
        sentiment_res = "Negative"
    else:
        sentiment_res = "Neutral"

    return sentiment_res

def dataentry(title, text, result):
    li = [title, text, result]
    #44315 new data.... 

    with open('./notebook_work/dataframe.csv', 'a+', newline='') as w:
        writer_obj = writer(w)
        writer_obj.writerow(li)

        w.close()