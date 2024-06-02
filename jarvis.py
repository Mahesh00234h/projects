import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
import json
import pyjokes


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(audio):
    """Function to convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Function to greet the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. Please tell me how may I help you")

def takeCommand():
    """Function to take voice input from the user and convert it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        r.energy_threshold = 300
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=30, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def searchWikipedia(query):
    """Function to search Wikipedia and speak the summary."""
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any results on Wikipedia.")
    except Exception as e:
        speak("Sorry, something went wrong while searching Wikipedia.")

def openWebsite(url, site_name):
    """Function to open a website."""
    speak(f"Opening {site_name}")
    webbrowser.open(url)

def playMusic():
    """Function to play a specific YouTube video."""
    youtube_url = 'https://youtu.be/m7_3Xn95xvg?si=zZRBVTA-dPU2HyLu'
    try:
        webbrowser.open(youtube_url)
        speak("Playing the video on YouTube.")
    except Exception as e:
        speak("Sorry, I couldn't open the YouTube video.")

def tellTime():
    """Function to tell the current time."""
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time is {strTime}")

def getWeather():
    """Function to get the current weather."""
    api_key = "401609890a9475afd8b17849fc5443c0" 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Please tell me the city name")
    city_name = takeCommand().lower()
    if city_name == "none":
        speak("I didn't catch the city name. Please try again.")
        return

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        try:
            main = data["main"]
            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_desc = data["weather"][0]["description"]
            temp_celsius = temperature - 273.15
            speak(f"The temperature in {city_name} is {temp_celsius:.2f} degrees Celsius, "
                  f"with {weather_desc}. The humidity is {humidity}% and the pressure is {pressure} hPa.")
        except KeyError:
            speak("Sorry, I couldn't retrieve the weather information. Please try again later.")
    else:
        speak("City not found. Please try again.")

def getNews():
    """Function to get the latest news headlines."""
    api_key = "4d7f47550eee45c7b374149b560ef561" 
    base_url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=" + api_key
    response = requests.get(base_url)
    data = response.json()
    articles = data["articles"]
    speak("Here are the top news headlines:")
    for i, article in enumerate(articles[:5]):
        speak(f"Headline {i+1}: {article['title']}")

def tellJoke():
    """Function to tell a joke."""
    joke = pyjokes.get_joke()
    speak(joke)

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if query == "none":
            continue

        if 'wikipedia' in query:
            searchWikipedia(query)
        elif 'open youtube' in query:
            openWebsite("https://youtube.com", "YouTube")
        elif 'open google' in query:
            openWebsite("https://google.com", "Google")
        elif 'search for' in query:
            search_query = query.replace("search for", "").strip()
            if search_query:
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                speak(f"Searching Google for {search_query}")
            else:
                speak("Sorry, I didn't catch what you want to search for on Google. Please try again.")
        elif 'open stack overflow' in query:
            openWebsite("https://stackoverflow.com", "Stack Overflow")
        elif 'open linkedin' in query:
            openWebsite("https://linkedin.com", "LinkedIn")
        elif 'open codechef' in query:
            openWebsite("https://codechef.com", "CodeChef")
        elif 'open code' in query:
            codePath = "C:\\Users\\Asus\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        elif 'what is the time' in query or 'what the time' in query:
            tellTime()
        elif 'play music' in query:
            playMusic()
        elif 'open web' in query:
            open_web = query.replace("open web", "").strip()
            if open_web:
                webbrowser.open(f"https://www.google.com/search?q={open_web}")
                speak(f"Opening {open_web} search results")
            else:
                speak("Sorry, I didn't catch what you want to open. Please try again.")
        elif 'weather' in query:
            getWeather()
        elif 'news' in query:
            getNews()
        elif 'tell me a joke' in query or 'tell a joke' in query:
            tellJoke()


        elif 'exit' in query or 'stop' in query:
            speak("Goodbye Sir, have a nice day!")
            break
        else:
            speak("Sorry, I didn't catch that. Could you please repeat?")
