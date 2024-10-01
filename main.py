import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import os
import smtplib
import sys
import time
import schedule
import subprocess

# Initialize the speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice command
def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
        except Exception as e:
            print(f"Error: {str(e)}")
            return ""
    return command.lower()

# Function to handle the recognized command
def handle_command(command):
    if 'open' in command:
        # Extract the website name from the command
        website = command.replace('open ', '').strip().lower()
        url = f'https://www.{website}.com'
        
        try:
            webbrowser.open(url)
            talk(f"Opening {website}")
        except Exception as e:
            talk(f"Sorry, I couldn't open {website}")
            print(f"Error opening website: {e}")

    elif 'open file' in command:
        file_path = 'C:/Users/12109/Documents/Fall_2024/Programming Languages/Eye_Spy/Eye-Spy/test.txt'
        if os.path.exists(file_path):
            os.startfile(file_path)
            talk(f"Opening {file_path}")
        else:
            talk(f"File not found: {file_path}")

    elif 'search' in command:
        search_query = command.replace('search', '').strip()
        pywhatkit.search(search_query)
        talk(f"Searching for {search_query}")

    elif 'send email' in command:
        send_email('recipient_email@gmail.com', 'Test Subject', 'This is a test email.')

    elif 'reminder' in command:
        reminder_text = command.replace('set reminder', '').strip()
        time_of_day = input("Please specify the time (HH:MM format) for the reminder: ")
        set_reminder(reminder_text, time_of_day)

    elif 'exit' in command or 'stop' in command:
        talk("Closing the assistant. Goodbye!")
        sys.exit()  # Exits the program

    else:
        talk("Sorry, I didn't get that.")

# Function to send an email
def send_email(to_address, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    email_message = f"Subject: {subject}\n\n{message}"
    server.sendmail('your_email@gmail.com', to_address, email_message)
    server.close()
    talk("Email sent successfully")

# Function to set a reminder
def set_reminder(reminder_text, time_of_day):
    schedule.every().day.at(time_of_day).do(lambda: talk(f"Reminder: {reminder_text}"))
    talk(f"Reminder set for {time_of_day} to {reminder_text}")

# Function to check reminders
def check_reminders():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Function to run the assistant
def run_assistant():
    command = get_voice_command()
    if command:
        handle_command(command)

# Main loop for reminders and the assistant
if __name__ == '__main__':
    # Run assistant in one thread and check reminders in another
    while True:
        run_assistant()
        check_reminders()
