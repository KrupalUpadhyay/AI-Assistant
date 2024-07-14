from flask import Flask, render_template, request, jsonify
import pyttsx3
import json
import datetime

app = Flask(__name__)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def load_qa_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

qa_data = load_qa_data('qa_data.json')

def search_and_speak(query, qa_data):
    max_matches = 0
    best_match = None
    for question in qa_data.keys():
        common_words = set(question.lower().split()) & set(query.lower().split())
        num_matches = len(common_words)
        if num_matches > max_matches:
            max_matches = num_matches
            best_match = question

    if best_match:
        answer = qa_data[best_match]
        return answer
    else:
        return "Sorry, I couldn't find an answer."

def wish_me():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        return "Good Morning, Sir!"
    elif hour >= 12 and hour < 18:
        return "Good Afternoon, Sir!"
    else:
        return "Good Evening, Sir!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['GET'])
def greet():
    greeting = wish_me()
    speak(greeting)
    return jsonify({'response': greeting})

@app.route('/username', methods=['GET'])
def username():
    prompt = "What should I call you, sir?"
    speak(prompt)
    return jsonify({'response': prompt})

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['query']
    response = search_and_speak(user_input, qa_data)
    speak(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
