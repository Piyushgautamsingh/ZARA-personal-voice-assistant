import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from sys import exit
from googlesearch import search
import urllib
import re
import time
import requests
import subprocess
from pyowm import OWM


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    time.sleep(1)
    engine.runAndWait()

def wishME():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("...hey...what..i can do for you! ")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio).lower()
        print(f"You said: {query}\n")
    except sr.UnknownValueError:
        speak("Sorry,..say again please...")
        command = takeCommand();
        return command
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

        elif 'open google' in query:
            webbrowser.open("https://www.google.co.in")
            query = "go to sleep"

        elif 'open whatsapp' in query:
            speak("opening whatsapp...")
            webbrowser.open("https://web.whatsapp.com/")
            query = "go to sleep"

        elif 'current weather' in query:
            reg_ex = re.search('current weather in (.*)', query)
            if reg_ex:
                city = reg_ex.group(1)
                owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
                obs = owm.weather_at_place(city)
                w = obs.get_weather()
                k = w.get_status()
                x = w.get_temperature(unit='celsius')
                speak('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (
                    city, k, x['temp_max'], x['temp_min']))
        elif 'play music' in query:
            music_dir = 'C:\\Users\Piyush Gautham\Downloads\Video\Music Fav'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
            query = takeCommand().lower()
        elif 'tell me a joke' in query:
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept": "application/json"})
            if res.status_code == requests.codes.ok:
                print(str(res.json()['joke']))
                speak(str(res.json()['joke']))
                takeCommand()
            else:
                speak('oops!I ran out of jokes')

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")
            query = takeCommand().lower()

        elif "who is your father"  in query:
            s="Piyush Singh"
            speak(f"Hey! My Father name is{s}")
            query = takeCommand().lower()

        elif "google" in query:
            speak('Searching google...')
            query = query.replace("google", "")
            for url in search(query, tld="co.in", num=1, stop=1, pause=2):
                webbrowser.open("https://google.com/search?q=%s" % query)
            takeCommand()
        elif 'youtube' in query:
            speak('Ok!')
            reg_ex = re.search('youtube (.+)', query)
            if reg_ex:
                domain = query.split("youtube", 1)[1]
                query_string = urllib.parse.urlencode({"search_query": domain})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})',html_content.read().decode())
                webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            else:
                pass

        elif 'open' in query:
            reg_ex = re.search('open (.+)', query)
            if reg_ex:
                domain = reg_ex.group(1)
                print(domain)
                url = 'https://www.' + domain
                webbrowser.open(url)
                speak('The website you have requested has been opened for you Sir.')
            else:
                pass
        elif 'tell about you' or 'hi' or 'hello' in query:
            speak('Hi sir, I am Zara and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')
            query = takeCommand().lower()

        elif 'launch' in query:
            reg_ex = re.search('launch (.*)', query)
            if reg_ex:
                appname = reg_ex.group(1)
                appname1 = appname + ".app"
                subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
                speak('I have launched the desired application')
        elif 'shutdown' in query:
            speak('Bye bye Sir. Have a nice day')
            exit(0)
        elif 'help me' in query:
            speak("""
            You can use these commands and I'll help you out:
            1.  Say wikipedia your query
            2.  Open Google
            3.  Open Whatsapp
            4.  Current weather in {cityname} : Tells you the current condition and temperture
            5.  Play music
            6.  Tell me a joke
            7.  Time : Current system time
            8.  who is your father
            9.  Search Google somthing :6Say Google your query it
            10. Play Song form YouTube: Say your query youtube
            11. Open xyz.com : replace xyz with any website name
            12. To know about me:Tell about you or Hello or hey
            13. Launch your query Applications
            14. To Stop me: Say Shutdown
            """)

        else:
            speak("Sorry I don't know that... you can  google it")
            query = takeCommand().lower()
