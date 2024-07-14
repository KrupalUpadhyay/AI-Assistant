import pyttsx3
import speech_recognition as sr
import os
import random
import wikipedia
import webbrowser
import json
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...........")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing.....")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please try again.")
            return "None"
        except sr.UnknownValueError:
            speak("Unable to recognize your voice...")
            return "None"
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't understand. Can you repeat that?")
            return "None"
        return query


def username():
    speak("What should I call you, sir?")
    uname = takeCommand()
    speak("Welcome, Mister " + uname)
    speak("How can I help you, Sir?")


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning, Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, Sir!")
    else:
        speak("Good Evening, Sir!")
    speak("I am your virtual Assistant, Mia!")

def load_qa_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load question-answer data from JSON file
file_path = 'qa_data.json'
qa_data = load_qa_data(file_path)

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
        speak(answer)
    else:
        speak("Sorry, I couldn't find an answer.")

if __name__ == '__main__':
    wishMe()
    username()
    
    while True:
        query = takeCommand().lower()
        search_and_speak(query, qa_data)
