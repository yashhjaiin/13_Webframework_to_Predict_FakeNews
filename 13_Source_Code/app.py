from flask import Flask, request, render_template, redirect
from modules import *
from twitter_api import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def result():

    result = request.form
    title = result['title']
    text = result['text']
    val = preprocess(title, text)

    pred = predict(val)                             #news prediction
    sentiment_res = sentimentPrediction(title)                  #sentiments prediction

    return render_template('result.html', news_result=pred, sentiment_res=sentiment_res, title=title, text=text)

@app.route('/retrain', methods=['POST'])
def reTrain():

    retrain = request.form
    title = retrain['title']
    text = retrain['text']
    result = retrain['news_result']
    poll = retrain['poll']

    val = preprocess(title, text)

    #this function retrain the model if poll==correct || if poll==incorrect change the bit and then retrain
    result = 1 if result == 'REAL' else 0 
    print("Before Retraining ", pipeline.predict_proba_one(val))
    
    if poll == 'correct':
        pipeline.learn_one(val, result)
        print("After Retraining ", pipeline.predict_proba_one(val))

    else:
        result = 0 if result == 1 else 1
        pipeline.learn_one(val, result)
        print("After Retraining ", pipeline.predict_proba_one(val))

    dataentry(title, text, result)

    return redirect('/')

@app.route('/tweet')
def tweet():
    tweets_collection = getData()
        
    return render_template('api_data.html', tweets=tweets_collection)

if __name__ == '__main__':
    app.run(debug=True)