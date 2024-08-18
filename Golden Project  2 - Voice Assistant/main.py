# Description: This is a simple voice assistant that can add tasks to a list, show tasks in the list, take a screenshot, and open Chrome.
import speech_recognition as sr
from gtts import gTTS
import winsound
import os
from pydub import AudioSegment
import pyautogui
import webbrowser

# Function to listen to the user's voice command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, show_all=False)
        print("You said: ", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError:
        print("Unable to access Google Speech Recognition API.")
        return None

# Function to respond to the user's command
def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang="en")
    temp_mp3 = "response.mp3"
    temp_wav = "response.wav"
    tts.save(temp_mp3)
    sound = AudioSegment.from_mp3(temp_mp3)
    sound.export(temp_wav, format="wav")
    winsound.PlaySound(temp_wav, winsound.SND_FILENAME)
    
    os.remove(temp_mp3)
    os.remove(temp_wav)

# Main Variables
tasks = []
listening_to_task = False

# Function to add a task to the list
def add_task():
    global listening_to_task
    listening_to_task = True
    respond("What task would you like to add?")

# Function to show the tasks in the list
def show_tasks():
    if not tasks:
        respond("You have no tasks.")
    else:
        respond(f"You have {len(tasks)} tasks.")
        for task in tasks:
            respond(task)

# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    respond("Screenshot saved.")

# Function to open Chrome
def open_chrome():
    webbrowser.open("https://www.google.com")
    respond("Chrome is open.")

# Main function
def main():
    global listening_to_task

    command_handlers = {
        "add a task": add_task,
        "task list": show_tasks,
        "take a screenshot": take_screenshot,
        "open chrome": open_chrome,
        "exit": lambda: respond("Goodbye!") or exit()
    }

    while True:
        command = listen()
        triggerKey = "hey assistant"

        if command and triggerKey in command:
            if listening_to_task:
                tasks.append(command)
                listening_to_task = False
                respond(f"Adding '{command}' to your tasks. You have {len(tasks)} tasks in total.")
            else:
                handler = command_handlers.get(command, lambda: respond("I'm sorry, I did not understand the command."))
                handler()

# Run the main function
if __name__ == "__main__":
    main()
