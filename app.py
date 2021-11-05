import nltk
import re
import string
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('Home.html', title="Home")


@app.route('/', methods=['POST'])
def my_form_post():
    if request.method == 'POST':
        text = request.form['text']
        nltk.download('vader_lexicon')
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        sid = SentimentIntensityAnalyzer()
        score = (sid.polarity_scores(str(text)))['compound']

        if score > 0:
            label = 'Positive'
        elif score == 0:
            label = 'Neutral'
        else:
            label = 'Negative'

    return render_template('Home.html', result=label)


@app.route('/analysis')
def view_analysis():
    data = pd.read_csv('final-sentiment-data.csv', header=0)
    myData = list(data.values)
    return render_template('Analysis.html', title="Analysis", myData=myData)


if __name__ == '__main__':
    app.debug = True
    app.run()
