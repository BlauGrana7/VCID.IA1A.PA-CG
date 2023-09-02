# Diese Datei enthält die Daten, Funktionen und Variablen, welche in app.py verwendet werden.
import io
import base64
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import numpy as np

matplotlib.use('Agg')

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="survey_db"
)
# Die Fragen der Umfrage
questions = [
    "Wie zufrieden waren Sie mit der Ausbildung insgesamt?",
    "Wie würden Sie die Qualität der Dozenten bewerten?",
    "Wie bewerten Sie die Infrastruktur der Schule?",
    "Hat Ihnen die Ausbildung geholfen, Ihre beruflichen Ziele zu erreichen",
    "Wie empfinden Sie die Vorbereitung auf IT-Zertifizierungsprüfungen im Rahmen Ihrer Ausbildung?",
    "Wie empfinden Sie die Vorbereitung im Unterricht auf die Praxisarbeiten Ihrer Ausbildung?",
    "Wie war die Gewichtung von Praxis zum Theorieteil während des Unterrichts?",
    "Wie herausfordernd haben Sie die Ausbildung empfunden?",
    "Welchen Beschäftigungsgrad hatten Sie während der Ausbildung?",
    "Welchen Beschäftigungsgrad würden Sie für die Ausbildung empfehlen?",
    "Wie haben Sie den Online-Unterricht im Vergleich zum Präsenz-Unterricht empfunden?",
    "Wie wahrscheinlich würden Sie die Ausbildung weiterempfehlen?",
    "Welche Fächer waren nicht nötig oder nicht für ihre Tätigkeit nützlich?",
    "Welche Inhalte der Ausbildung hätten Sie gerne tiefer behandelt im Unterricht/oder haben sogar gefehlt?",
    "Haben Sie Verbesserungsvorschläge für die Ausbildung?"
]

# List of options for MCQ-based questions
mcq_options = [
    ["Sehr zufrieden", "Zufrieden", "Unzufrieden", "Sehr unzufrieden"],
    ["Sehr Kompetent", "Kompetent", "Eher Kompetent", "Nicht Zufriedenstellend"],
    ["Sehr gut", "Gut", "Aktzeptabel", "Schlecht"],
    ["Ja", "Eher ja", "Eher nein", "Nein"],
    ["Sehr gut", "Gut", "Aktzeptabel", "Schlecht"],
    ["Ja", "Eher ja", "Eher nein", "Nein", "Nein überhaupt nicht"],
    ["Praxis dominierte", "Gleichgewicht zwischen Praxis und Theorie", "Theorie dominierte", "Keine Praxiserfahrung"],
    ["Sehr herausfordernd", "Herausfordernd", "Angemessen", "Eher einfach", "Sehr einfach"],
    ["100%", "90%", "80%", "70%", "50%"],
    ["100%", "90%", "80%", "70%", "50%"],
    ["Sehr gut", "Gleichwertig", "Eher schlechter", "Schlechter", "Je nach Dozent"],
    [1,2,3,4,5,6,7,8,9,10]
]
# Folgende Funktionen werden in app.py für die grafische Darstellung der Admin-Seite gebraucht


def plot_handler(column):
    query = f"SELECT `{column}` FROM survey"
    data = pd.read_sql_query(query, mydb)

    # Zählt die Häufigkeit jeder Antwort
    option_counts = data[column].value_counts()

    plt.figure()
    plt.bar(option_counts.index, option_counts.values, width=0.4)
    plt.xlabel('Antwortmöglichkeit')
    plt.ylabel('Anzahl Antwort')
    plt.title(column)
    plt.tight_layout()
    # Minimum der y-axis setzen
    min_limit = 0 
    plt.ylim(bottom=min_limit)
    plt.grid(True)
    # y_ticks = range(int(option_counts.min()), int(option_counts.max()) + 1, 1)
    # plt.yticks(y_ticks)


def create_plot():
    plot_strings_list = []
    plot_handler('Infrastruktur')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    plot_handler('Praxis/Theorie')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    plot_handler('Beschaeftigungsgrad Empfehlung')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    plot_handler('Weiterempfehlung von 1-10')
    img_b64 = plot_to_img()
    str = "data:image/png;base64,"+img_b64
    plot_strings_list.append(str)

    return plot_strings_list


def plot_to_img():  # Konvertiert plot to img

    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Konvertiert BytesIO object to base64 string
    img_b64 = base64.b64encode(img.getvalue()).decode()

    return img_b64
