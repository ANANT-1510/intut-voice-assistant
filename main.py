import pyautogui
import speech_recognition as sr
import pyttsx3  # Added for Windows TTS support
import os
import webbrowser
import keyboard
import pygetwindow as gw
import re
import sys
import pywhatkit
import subprocess
from datetime import datetime
import google.generativeai as genai  # Import Google Gemini API
from google import genai



engine = pyttsx3.init()

def wishMe():
    now = datetime.now()
    hour = int(now.strftime("%H "))
    print(hour)
    if(hour<12):
        say("Good Morning Sir")
    elif(hour>=12 and hour<=16):
        say("Good Afternoon Sir")
    else:
        say("Good Evening Sir")
def is_app_running(process_name):
    result = subprocess.run(['tasklist'], capture_output=True, text=True)
    return process_name.lower() in result.stdout.lower()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.8)  # Adjusts noise threshold
        r.pause_threshold = 1.0
        r.sample_rate=48000
        r.phrase_threshold=0.5
        # r.dynamic_energy_threshold=True
        # r.dynamic_energy_adjustment_damping=2
        # r.energy_threshold=4000
        audio = r.listen(source,timeout=8, phrase_time_limit=10)
        try:
            print("Recognizing")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occurred. Sorry from my side"
        
def chat_with_gemini(prompt):
    try:
        

        client = genai.Client(api_key="AIzaSyDbES7X4EBUxeGaoAYRwT58G2bnoqJAIRk")
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
            )
        response_text=response.text
        save_response_to_file(prompt, response_text)
        print(response.text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"  # Print error message


def save_response_to_file(query, response):
    folder_path = "Gemini_Responses"  # Folder where responses will be stored
    os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Unique filename with date-time
    file_path = os.path.join(folder_path, f"{query}_{timestamp}.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Query: {query}\n\nResponse:\n{response}")


if __name__ == '__main__':
    say("Hello, I am intut")
    speak=True
    while speak:
        print("Listening...")
        query = takeCommand()

        if "hey" in query.lower() or "hello" in query.lower() or "hi" in query.lower():
            wishMe()

        elif "play youtube" in query.lower():
            pattern = r"(play(?: the song)? )(.*?)( on youtube|$)"
            match = re.search(pattern, query.lower())

            if match:
                song_name = match.group(2).strip()
                say(f"Playing {song_name} on YouTube.")
                pywhatkit.playonyt(song_name)
            else:
                say("Couldn't recognize the song name.")


        
        elif "date" in query.lower():
            current_date = datetime.now().strftime("%A, %d %B %Y")
            say(f"Sir, the date is {current_date}")

        elif "time" in query.lower():
            now = datetime.now()
            hour = now.strftime("%I").lstrip("0")
            minute = now.strftime("%M")
            meridiem = now.strftime("%p")
            say(f"Sir, the time is {hour} {minute} {meridiem}")

        elif "volume up" in query.lower() or "increase volume" in query.lower():
            pyautogui.press("volumeup")
            say("Volume Increased")

        elif "volume down" in query.lower() or "dcrease volume" in query.lower():
            pyautogui.press("volumedown")
            say("Volume Decreased")
        elif "volume mute" in query.lower() or "mute volume" in query.lower():
            pyautogui.press("volumemute")
            say("Volume Muted")

        elif "open vs code" in query.lower():
            os.system(r'start "" "C:\\Users\\KIIT\\Desktop\\Visual Studio Code.lnk"')
            say("Opening VS Code")

        elif "open telegram" in query.lower():
            os.system(r'start "" "C:\Users\KIIT\Desktop\Telegram Desktop\tupdates\temp\Telegram.exe"')
            say("Opening Telegram")

        # elif "close vs code" in query.lower():
        #     process_name = "Code.exe"  # VS Code's main process name
        #     if is_app_running(process_name):
        #         os.system(f"taskkill /f /im {process_name}")  # Force close VS Code
        #         say("Closing VS Code")
        #     else:
        #         say("VS Code is already closed.")

        elif "lock screen" in query.lower():
            os.system("rundll32.exe user32.dll,LockWorkStation")
            say("Locking the screen now.")


        elif "open" in query.lower():
            commands = {
                "calculator": "start calc",
                "notepad": "start notepad",
                "command prompt": "start cmd",
                "file explorer": "start explorer",
                "task manager": "start taskmgr",
                "paint": "start mspaint",
                "wordpad": "start write",
                "snipping tool": "start snippingtool",
                "powershell": "start powershell",
                "settings": "start ms-settings:"
            }

            match = re.search(r'open (.+?)( for me| please| now|$)', query.lower())

            if match:
                site = match.group(1).strip()
                for app in commands:
                    if app in site:
                        os.system(commands[app])
                        say(f"Opening {app}")
                        break
                else:
                    webbrowser.open(f"https://{site}.com")
                    say(f"Opening {site}")
            else:
                say("Sorry, I couldn't understand what to open.")

        elif "google" in query.lower():
            match = re.search(r'(?:what is|who is) (.+)', query.lower())  # Extract the search term
            cleaned_query = re.sub(r'\s*(google|using google)\b', '', query, flags=re.IGNORECASE).strip()
            webbrowser.open(f"https://www.google.com/search?q={cleaned_query}")  # Open Google search
            say(f"Searching for {query} on Google.")
            # if match:
            #     search_query = match.group(1).strip()
            #     webbrowser.open(f"https://www.google.com/search?q={search_query}")  # Open Google search
            #     say(f"Searching for {search_query} on Google.")
            # else:
            #     say("Sorry, I couldn't understand your question.")

        elif "close" in query.lower():
            app_processes = {
                "calculator": "CalculatorApp.exe",
                "notepad": "notepad.exe",
                "command prompt": "cmd.exe",
                "file explorer": "explorer.exe",
                "task manager": "Taskmgr.exe",
                "paint": "mspaint.exe",
                "wordpad": "wordpad.exe",
                "snipping tool": "SnippingTool.exe",
                "powershell": "powershell.exe",
                "settings": "SystemSettings.exe",
                "chrome": "chrome.exe",
                "edge": "msedge.exe",
                "firefox": "firefox.exe",
                "vs code": "Code.exe",
                "telegram": "Telegram.exe"
            }
            match = re.search(r'close (.+?)( for me| please| now|$)', query.lower())

            if match:
                site = match.group(1).strip().lower()

                if site in app_processes:
                    process_name = app_processes[site]
                    if is_app_running(process_name):
                        os.system(f"taskkill /f /im {process_name}")
                        say(f"Closing {site}")
                    else:
                        say(f"{site} is already closed.")

                else:
                  browser_windows = gw.getAllWindows()
                  tab_closed = False
                  
                  for window in browser_windows:
                      if site in window.title.lower():
                          window.minimize()
                          window.restore()  # Ensures tab is visible
                          keyboard.press_and_release('ctrl+w')  # Close the active tab
                          say(f"Closing {site}")
                          tab_closed = True
                          break
                  
                  if not tab_closed:
                      say(f"Sorry, I couldn't find a tab with {site} open.")

        
        
        elif "bye" in query.lower() or "shutdown" in query.lower() or "shut down" in query.lower():
            speak=False
            say("Bye Sir")
            sys.exit()
        elif "artificial intelligence" in query.lower() or "a.i" in query.lower() or "ai" in query.lower() or "gemini" in query.lower():
            cleaned_query = re.sub(r'\s*(ai|using ai)\b', '', query, flags=re.IGNORECASE).strip()
            response = chat_with_gemini(cleaned_query)
            say(response)