import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  
import requests
import os
import openai


recognizer = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
newsapi = "your_newsapi_key_here"  # Replace with your NewsAPI key


openai.api_key = "your_openai_api_key_here"  # Replace with your OpenAI API key

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Sorry, I encountered a problem processing your request."

def processCommand(command):
    print("Command received:", command)
    command = command.lower()

    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif "instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "whatsapp" in command:
        os.system("start whatsapp://")

    elif command.startswith("play"):
        parts = command.split(" ", 1)
        if len(parts) > 1:
            song = parts[1].strip()
            if song in musicLibrary.music:
                speak(f"Playing {song}")
                webbrowser.open(musicLibrary.music[song])
            else:
                speak(f"Sorry, I couldn't find {song} in your music library.")
        else:
            speak("Please specify a song name after 'play'.")

    elif "news" in command:
        r = requests.get(f"https://newsdata.io/api/1/latest?apikey={newsapi}&q=top%20headlines")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("results", [])
            if articles:
                speak("Here are the top headlines.")
                for article in articles[:5]:  # Limit to 5 headlines
                    speak(article.get('title', ''))
            else:
                speak("No headlines found.")
        else:
            print("Failed to fetch data. Status code:", r.status_code)
            speak("Unable to fetch the news at the moment.")

    else:
        # If not matched, ask OpenAI
        speak("Let me think...")
        response = aiProcess(command)
        print("AI Response:", response)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        print("Audio capture started.")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)

            word = recognizer.recognize_google(audio).lower()
            print("Heard:", word)

            if "jarvis" in word:
                speak("Hey boss")
                with sr.Microphone() as source:
                    print("Jarvis is active. Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=2)
                    command = recognizer.recognize_google(audio).lower()

                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
        except Exception as e:
            print(f"Unexpected error: {e}")