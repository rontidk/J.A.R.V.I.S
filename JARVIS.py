import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from groq import Groq
from gtts import gTTS
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Replace with your News API key
news_api = "Enter your own news API key."

def speak_old(txt):
    engine.say(txt)
    engine.runAndWait()

def speak(txt):
    tts = gTTS(txt)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# Replace with your Groq API key
client = Groq(api_key="Enter your own Groq API key.")

def ask_llama(prompt):
    """Ask Groq-hosted LLaMA for a quick response."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Jarvis, a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content


def process_command(c):
    if "goodbye jarvis" in c.lower():
        speak("Goodbye! Shutting down.")
        exit()
        
    elif "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://pk.linkedin.com/")

    elif "play" in c.lower():
        parts = c.split("play", 1)
        if len(parts) > 1:
            song = parts[1].strip().lower()
            matched_song = next((title for title in musiclibrary.music if title.lower() == song), None)
            if matched_song:
                webbrowser.open(musiclibrary.music[matched_song])
                speak(f"Playing {matched_song}")
            else:
                speak("This song is not in your music library.")

    elif "news" in c.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if articles:
                    for article in articles[:3]:
                        speak(article['title'])
                else:
                    speak("I couldn't find any news right now.")
            else:
                speak("Failed to fetch news. Please check the API key.")
        except Exception as e:
            speak(f"Error fetching news: {e}")

    elif c.lower().startswith("ask"):
        question = c.lower().replace("ask", "", 1).strip()
        if question:
            speak("Let me think...")
            answer = ask_llama("Answer in one sentence: " + question)
            speak(answer)
        else:
            speak("What should I ask LLaMA?")

if __name__ == "__main__":
    speak("JARVIS Initializing")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            wake_word = recognizer.recognize_google(audio)

            if wake_word.lower() == "jarvis":
                speak("Yes")
                print("Activated, listening for command...")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    process_command(command)

        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print(f"Speech Recognition error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
