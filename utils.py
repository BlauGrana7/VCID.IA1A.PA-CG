# Diese Datei enthält die Daten, Funktionen und Variablen, welche in app.py verwendet werden.
import io
import base64
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import numpy as np

matplotlib.use('Agg')  # Use a thread-safe backend

mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="pass",
    database="survey_db"
)
# Die Fragen der Umfrage
questions = [
    "Which area of computer science interests you the most?",
    "Which area of computer science do you find the most difficult?",
    "How do you find the quality of the teaching materials?",
    "How do you find the quality of the teaching?",
    "How satisfied are you with the organization of the training?",
    "Would you recommend the training?",
    "How would you rate the level of difficulty of the training?",
    "How often do you feel challenged by the training?",
    "How well do you feel prepared for the workforce after completing the training?",
    "How would you rate the diversity of the students in the training?",
    "How would you rate the support from the faculty and staff in the training?",
    "How likely is it that you would recommend this company to a friend or colleague?",
    "What are your strengths and weaknesses in relation to the training?",
    "What do you wish for the future of the training?",
    "What would you change about the training if you could?"
]

# List of options for MCQ-based questions
mcq_options = [
    ["System engineering", "Network engineering", "Cyber security", "Other"],
    ["System engineering", "Network engineering", "Cyber security", "Other"],
    ["Very good", "Good", "Satisfactory", "Not satisfied"],
    ["Very good", "Good", "Satisfactory", "Not satisfied"],
    ["Very satisfied", "Satisfied", "Unsatisfied", "Very unsatisfied"],
    ["Yes, definitely", "Yes, but with reservations",
        "No, rather not", "No, definitely not"],
    ["Very easy", "Easy", "Moderate", "Difficult", "Very difficult"],
    ["Very often", "Often", "Sometimes", "Rarely", "Never"],
    ["Very well prepared", "Well prepared", "Somewhat prepared",
        "Not prepared", "Not at all prepared"],
    ["Very diverse", "Diverse", "Somewhat diverse",
        "Not diverse", "Not at all diverse"],
    ["Very supportive", "Supportive", "Somewhat supportive",
        "Not supportive", "Not at all supportive"],
    [1,2,3,4,5,6,7,8,9,10]
]
# Folgende Funktionen werden in app.py für die grafische Darstellung der Admin-Seite gebraucht


def plot_handler(column):
    query = f"SELECT `{column}` FROM survey"
    data = pd.read_sql_query(query, mydb)

    # Count the occurrences of each response option
    option_counts = data[column].value_counts()

    plt.figure()
    plt.bar(option_counts.index, option_counts.values, width=0.4)
    plt.xlabel('Response Option')
    plt.ylabel('Number of Users who responded')
    plt.title(column)
    plt.tight_layout()
    # Set a minimum y-axis limit
    min_limit = 0  # Set this based on your preference
    plt.ylim(bottom=min_limit)
    plt.grid(True)
    # y_ticks = range(int(option_counts.min()), int(option_counts.max()) + 1, 1)
    # plt.yticks(y_ticks)


def create_plot():
    plot_strings_list = []
    plot_handler('Quality of Teaching')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    plot_handler('Level of Difficulty of Training')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    plot_handler('Diversity of Students in Training')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    plot_handler('Level of Recommendation of Company on 1-10 Scale')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    return plot_strings_list


def plot_to_img():  # converts plot to img

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert BytesIO object to base64 string
    img_b64 = base64.b64encode(img.getvalue()).decode()

    return img_b64
