import speech_recognition as sr
import webbrowser
import requests
from gtts import gTTS
import pygame
import os
import musicLibrary
import calculator
import timeModule  # <-- NEW TIME MODULE
from ai_service import ask_ai
# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
NEWS_KEY = "YOUR_NEWS_API_KEY"
# -------------------------------------------------------
# SPEECH OUTPUT
# -------------------------------------------------------
def speak(text):
    try:
        tts = gTTS(text)
        tts.save("temp.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print("Speak Error:", e)
# -------------------------------------------------------
# GROQ AI RESPONSE
# -------------------------------------------------------
def aiProcess(command):
    return ask_ai(command)
# -------------------------------------------------------
# COMMAND HANDLER
# -------------------------------------------------------
def processCommand(cmd):
    cmd = cmd.lower()
    # ---------- Exit ----------
    if "bye" in cmd or "goodbye" in cmd:
        speak("Goodbye Bhargav, shutting down.")
        exit(0)
    # ---------- Time Feature ----------
    if "time" in cmd or "current time" in cmd or "what time" in cmd:
        current_time = timeModule.get_time_ist()
        speak(current_time)
        return
    # ---------- Calculator ----------
    if calculator.looks_like_math(cmd):
        answer = calculator.calculate(cmd)
        speak(answer)
        return
    # ---------- Websites ----------
    if "open google" in cmd:
        webbrowser.open("https://google.com")
        speak("Opening Google")
        return
    elif "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
        return
    elif "open facebook" in cmd:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
        return
    elif "open linkedin" in cmd:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
        return
    # ---------- Songs ----------
    elif cmd.startswith("play"):
        try:
            song = cmd.replace("play", "").strip()
            link = musicLibrary.get_song_link(song)
            if not link:
                raise KeyError(song)
            speak(f"Playing {song}")
            webbrowser.open(link)
        except:
            speak("I cannot find that song in your library.")
        return
    # ---------- News ----------
    elif "news" in cmd:
        try:
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_KEY}"
            )
            data = r.json()
            if data.get("status") == "ok":
                for article in data.get("articles", []):
                    speak(article['title'])
            else:
                speak("Unable to fetch news.")
        except:
            speak("There was an error fetching news.")
        return
    # ---------- AI fallback ----------
    else:
        reply = aiProcess(cmd)
        speak(reply)
        return
# -------------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------------
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    speak("Hi Bhargav. Say 'Maya' to activate me.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
            text = recognizer.recognize_google(audio).lower()
            print("Heard:", text)
            if "maya" in text or "maaya" in text or "mya" in text:
                speak("Yes Bhargav?")
                print("Maya activated...")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=5)
                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print("Error:", e)
