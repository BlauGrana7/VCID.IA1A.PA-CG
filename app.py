from flask_restful import Api, Resource
import matplotlib.pyplot as plt
import mysql.connector
from flask import session, jsonify, url_for, Flask, render_template, request, redirect
import json
from utils import questions, mcq_options, create_plot
import requests
from flask_session import Session
import pandas as pd
import matplotlib#zum anzeigen der Grafiken
matplotlib.use('Agg')  

app = Flask(__name__)
api = Api(app)  # Für die Nutzung von Restful API

app.config['SESSION_TYPE'] = 'filesystem'  # zur Nutzung von file-based session storage

app.config['SECRET_KEY'] = 'your-secret-key'

# Starten der Session
Session(app)

mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="pass",
    database="survey_db"
)
mycursor = mydb.cursor()


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/signup')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        # authentifizierung
        sql = "select count(*) from user where email=%s and password=%s"
        # query um den Benutzernamen durch die email und das passwort zu finden
        sql2 = "select username from user where email=%s and password=%s"
        email = request.form.get('email')
        password = request.form.get('password')
        data = (email, password)
        # löst sql query aus
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        
        mycursor.execute(sql2, data)
        username = (mycursor.fetchall())[0][0]
        mydb.commit()
        print(result[0][0])
        if result[0][0] > 0:
            # lädt die session neu, weil ein neuer user in der session ist
            session["email"] = email
            session["user"] = username
            session["answers"] = {}  # speichert alle antworter mit dem eingeloggten user
            # wenn der user korrekt ist, weiter zum user panel
            return redirect(url_for("user_panel", id=1))
        else:
            # elif invalid user,neuer versuch mit fehlermeldung
            return redirect(url_for('signup', error="Invalid login", key=False))
  
    return render_template('login.html', key=True, error=None)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = request.args.get("error")  # fehlermledung
    key = request.args.get("key")  

    if request.method == "POST": 
        sql = "select count(*) from user where email=%s"
        username = request.form.get("username")
        email = request.form.get('email')
        password = request.form.get('password')
        data = (email,)
        # folgende lines führen sql query aus
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        if result[0][0] > 0:
            return redirect(url_for('signup', error="Email Already Exists", key=False))
        else:
            # wenn der Benutzer mit der email nicht existiert, speichern wir die werte in der Datenbank
            # und erstellen einen neuen User
            sql = "insert into user values(%s,%s,%s)"
            data = (username, email, password)
            # folgende lines führen sql query aus
            mycursor = mydb.cursor()
            mycursor.execute(sql, data)
            mydb.commit()
            return render_template('login.html', key=True,  error=None)
  
    return render_template('login.html', key=key, error=error)


@app.route('/user_panel/<int:id>', methods=['GET', 'POST'])
def user_panel(id):
    if request.method == "POST":  
        
        form_dict = request.form.items()
        for key, value in form_dict:
            session["answers"][key] = value

    if id == 1:
        question_options = zip(questions[:5], mcq_options[:5])
        return render_template("survey_form.html", textarea_questions="", question_options=question_options, progress=0, questions=questions)

    elif id == 2:
        question_options = zip(questions[5:10], mcq_options[5:10])
        return render_template("survey_form.html", textarea_questions=[], question_options=question_options, progress=33, questions=questions)

    else:
        question_options = zip(questions[10:12], mcq_options[10:12])
        text_qs = questions[12:16]
        return render_template("survey_form.html", textarea_questions=text_qs, question_options=question_options, progress=66, questions=questions)


class SurveyAPI(Resource):
    def get(self):#Wenn wir Daten von einer API abrufen möchten
        user_answers = {
            session.get("user"): session.get("answers")
        }
        return jsonify(user_answers)

    def post(self):#Wenn wir Daten an eine API senden möchten
        user_answers = {
            session.get("user"): session.get("answers")
        }
        return jsonify(user_answers)


api.add_resource(SurveyAPI, '/survey_api')


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.clear()
    return redirect('/signup')


@app.route('/post_survey', methods=['GET', 'POST'])

def post_survey():
    
    if request.method == "POST":  
        form_dict = request.form.items()
        for key, value in form_dict:
            session["answers"][key] = value
    data = [session["email"], session["user"]]

    mycursor = mydb.cursor()
    
    for i in range(12):
        key = str(i)
        
        data.append((session.get("answers"))[key])

    # Text antworten
    data.append(request.form.get("text1"))
    data.append(request.form.get("text2"))
    data.append(request.form.get("text3"))
    print(data)
    # sql query:
    sql = "insert into survey values (%s, %s , %s ,%s , %s , %s , %s , %s ,%s , %s , %s, %s , %s ,%s , %s , %s, %s) "
    
    mycursor.execute(sql, data)
    mydb.commit()

    requests.post("http://127.0.0.1:5000/survey_api")
    return render_template('successpage.html')

# AdminTeil


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():  # gleich wie oben
    if request.method == "POST":
        
        sql = "select count(*) from admin where email=%s and password=%s"

        email = request.form.get('email')
        password = request.form.get('password')
        data = (email, password)
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        print(result[0][0])
        if result[0][0] > 0:
            # mit admin zum admin-panel
            return redirect(url_for("admin_panel"))
        else:
            # elif invalid user,gleiche Fehlermeldungen
            return redirect(url_for('signup', error="Invalid login", key=False))
   
    return render_template("admin_login.html")


@app.route('/admin', methods=['GET'])
def admin_panel():
    list = create_plot() #function importiert aus utils.py
    sql = "select * from survey"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mydb.commit()
    return render_template("admin_page.html", str_list=list, answers=result)

app.run(debug=True,host='0.0.0.0',port=5000)
