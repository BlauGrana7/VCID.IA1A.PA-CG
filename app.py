from flask_restful import Api, Resource
import matplotlib.pyplot as plt
import mysql.connector
from flask import session, jsonify, url_for, Flask, render_template, request, redirect
import json
from utils import questions, mcq_options, create_plot
import requests
from flask_session import Session
import pandas as pd
import matplotlib#for plotting graphs
matplotlib.use('Agg')  # Use a thread-safe backend

app = Flask(__name__)
api = Api(app)  # Für die Nutzung von Restful API

app.config['SESSION_TYPE'] = 'filesystem'  # Use file-based session storage
# which helps us use session as global environmental variable
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
        # authenticates user through below statement
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
        # retrieving username
        mycursor.execute(sql2, data)
        username = (mycursor.fetchall())[0][0]
        mydb.commit()
        print(result[0][0])
        if result[0][0] > 0:
            # updating session variables because new user is in session now
            session["email"] = email
            session["user"] = username
            session["answers"] = {}  # will store all answers of logged in user
            # if user is valid,then we go to user panel
            return redirect(url_for("user_panel", id=1))
        else:
            # elif invalid user,go again to sign up page with error msg
            return redirect(url_for('signup', error="Invalid login", key=False))
    # below line never gets executed in our case but it is just to avoid
    # error that function returns an invalid response
    return render_template('login.html', key=True, error=None)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = request.args.get("error")  # error msg
    key = request.args.get("key")  # key used for specific functionalities
    # through jinja templating

    if request.method == "POST": #executed when we have post request 
        # below statement checks whether a user with same email exists already
        sql = "select count(*) from user where email=%s"
        username = request.form.get("username")
        email = request.form.get('email')
        password = request.form.get('password')
        data = (email,)
        # following lines execute sql query
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        if result[0][0] > 0:
            return redirect(url_for('signup', error="Email Already Exists", key=False))
        else:
            # if user with email doesn't exist already, we store values in database
            # and make a new user
            sql = "insert into user values(%s,%s,%s)"
            data = (username, email, password)
            # following lines execute sql query
            mycursor = mydb.cursor()
            mycursor.execute(sql, data)
            mydb.commit()
            return render_template('login.html', key=True,  error=None)
    # when redirected from get request and url_for as in case of
    # invalid login ,then we have
    # a get request and below line is executed
    return render_template('login.html', key=key, error=error)


@app.route('/user_panel/<int:id>', methods=['GET', 'POST'])
def user_panel(id):# renders appropriate questions on appropriate pages and keep track of pages using id parameter
    if request.method == "POST":  # if request made through form's next button,then
        # populate answers of current page in session
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
    def get(self):#when we want to fetch data from api
        user_answers = {
            session.get("user"): session.get("answers")
        }
        return jsonify(user_answers)

    def post(self):#when we want to post data to api
        user_answers = {
            session.get("user"): session.get("answers")
        }
        return jsonify(user_answers)


api.add_resource(SurveyAPI, '/survey_api')


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.clear()#clears user session's all things 
    return redirect('/signup')


@app.route('/post_survey', methods=['GET', 'POST'])
# this function populates database
def post_survey():
    # data to be stored in database
    if request.method == "POST":  # if request made through form's submit button at last,then
        # populate answers of current page in session
        form_dict = request.form.items()
        for key, value in form_dict:
            session["answers"][key] = value
    data = [session["email"], session["user"]]

    mycursor = mydb.cursor()
    # making answers dictionary to store answers got from database
    for i in range(12):
        key = str(i)
        # appending answers sequence wise to data list
        data.append((session.get("answers"))[key])

    # Now appending text based questions to data so that then data list
    # made above can be stored in database
    data.append(request.form.get("text1"))
    data.append(request.form.get("text2"))
    data.append(request.form.get("text3"))
    print(data)
    # sql query:
    sql = "insert into survey values (%s, %s , %s ,%s , %s , %s , %s , %s ,%s , %s , %s, %s , %s ,%s , %s , %s, %s) "
    # following lines execute sql query
    mycursor.execute(sql, data)
    mydb.commit()

    requests.post("http://127.0.0.1:5000/survey_api")
    return render_template('successpage.html')

# From now onwards ,whole code will be related to admin :


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():  # all logic like sign in function above, no need to worry
    if request.method == "POST":
        # authenticates user through below statement
        sql = "select count(*) from admin where email=%s and password=%s"

        email = request.form.get('email')
        password = request.form.get('password')
        data = (email, password)
        # following lines execute sql query
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        print(result[0][0])
        if result[0][0] > 0:
            # if admin is valid,then we go to admin panel
            return redirect(url_for("admin_panel"))
        else:
            # elif invalid user,go again to sign up page with error msg
            return redirect(url_for('signup', error="Invalid login", key=False))
    # if not post request ,mean if request from user login page ,then
    # simply go to login page
    return render_template("admin_login.html")


@app.route('/admin', methods=['GET'])
def admin_panel():
    list = create_plot() #function imported from utils.py
    sql = "select * from survey"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mydb.commit()
    return render_template("admin_page.html", str_list=list, answers=result)


app.run(debug=True)
