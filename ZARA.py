import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from sys import exit
from googlesearch import search
import  googlesearch

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishME():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("hey..handsome...... what..i can do for you! ")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

    except Exception as e:
        speak("Say that again please...")
        takeCommand()
        return "None"
    return query



if __name__ == '__main__':
    wishME()
    query = takeCommand().lower()
    while True:
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("Wikipedia")
            print(results)
            speak(results)
            query = takeCommand().lower()

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            query = "quit"

        elif 'open google' in query:
            webbrowser.open("https://www.google.co.in")
            query = "go to sleep"

        elif 'open codechef' in query:
            webbrowser.open("https://www.codechef.com")
            query = "go to sleep"

        elif 'open whatsapp' in query:
            speak("opening whatsapp...")
            webbrowser.open("https://web.whatsapp.com/")
            query = "go to sleep"

        elif 'play music' in query:
            music_dir = 'C:\\Users\Piyush Gautham\Downloads\Video\Music Fav'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
            query = takeCommand().lower()

        elif "what's the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            query = takeCommand().lower()

        elif "what's my name"  in query:
            s="Piyush"
            speak(f"Hey! Sexxy your name is{s}")
            query = takeCommand().lower()


        elif "go to sleep" in query:
            exit(0)
        elif "hello mom" in query:
            speak("Hey mom")
            query=takeCommand().lower()
        elif "google" in query:
            speak('Searching google...')
            query = query.replace("google", "")
            for url in search(query, tld="co.in", num=1, stop=1, pause=2):
                webbrowser.open("https://google.com/search?q=%s" % query)
            exit(0)
        else:
            speak("Sorry I don't know that... you can it google.... just say google...")
            query = takeCommand().lower()






