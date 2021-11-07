import pandas as pd
from flask import Flask, render_template, request
from sentiment_process import clean_text
import pickle
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db')
print("The database is accessed successfully")

conn.execute("CREATE TABLE if not exists sentiment_db (id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT,sentiment TEXT)")
print("Table created successfully")
conn.close()

model = pickle.load(open('model.pkl', 'rb'))
vectorized = pickle.load(open('vectorized.pkl', 'rb'))


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('Home.html', title="Home")


@app.route('/result', methods=['POST'])
def my_form_post():
    global conn, label
    text = request.form['text']
    print('Text: ', text)
    cleaned_text = clean_text.text_cleaner(text)
    test_bag = vectorized.transform([cleaned_text]).toarray()
    prediction = model.predict(test_bag)
    print('Prediction: ', prediction)
    if prediction == ['Positive']:
        label = 'Positive'
    elif prediction == ['Negative']:
        label = 'Negative'
    else:
        label = 'Neutral'
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO sentiment_db(text,sentiment) VALUES (?,?)", (text, label))
        conn.commit()
        feedback_id = cur.lastrowid
        return render_template('result.html', text=text, result=label, feedback_id=feedback_id)
    except:
        print("Error detected")
        conn.rollback()
    finally:
        conn.close()


@app.route('/analysis')
def view_analysis():
    data = pd.read_csv('final-sentiment-data.csv', header=0)
    myData = list(data.values)
    return render_template('Analysis.html', title="Analysis", myData=myData)


@app.route('/data')
def view_data():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from sentiment_db")

    rows = cur.fetchall()
    return render_template("data.html", title="Data", rows=rows)


if __name__ == '__main__':
    app.debug = True
    app.run()
