import ctypes
import datetime
import os
import shutil
import subprocess
import time
#import tkinter as tk
import webbrowser
# import png
import pyjokes
import pyqrcode
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import wikipedia
import winshell as winshell
from twilio.rest import Client
import sys
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, \
    QInputDialog
import threading

class MainWindow(QWidget):

    recognizer =sr.Recognizer()
    engine = pyttsx3.init()
    listener = sr.Recognizer()
    engine = pyttsx3.init('sapi5')
    listener.energy_threshold = 4000
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)


    def __init__(self):
        super().__init__()
        # Set window properties
        self.setWindowTitle('Voice Recognition')
        self.setGeometry(400, 400, 800, 600)

        # Create text boxes
        self.text_edit = QLineEdit(self)
        self.textbox2 = QLineEdit(self)

        # Create buttons
        self.button1 = QPushButton('Start Recording', self)
        self.button2 = QPushButton('submit', self)
        self.quit_button = QPushButton('Quit', self)

        # Connect buttons to functions
        self.button1.clicked.connect(self.run)
        #self.button2.clicked.connect(self.stop_listening)
        # self.quit_button.clicked.connect(self.quit_application)

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Enter command:'))
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button1)
        layout.addWidget(QLabel('Result:'))
        layout.addWidget(self.textbox2)
        layout.addWidget(self.button2)
        layout.addWidget(self.quit_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('Transcript:'))
        self.transcript_textbox = QTextEdit(self)
        right_layout.addWidget(self.transcript_textbox)
        self.transcript_textbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Set the read-only property to True
        self.transcript_textbox.setReadOnly(True)

        main_layout = QHBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(right_layout)

        # Set layout
        self.setLayout(main_layout)
        self.show()



        # Create the text output area

        self.greetings()
    def run(self):
        thread2 = threading.Thread(target=self.start)
        thread2.start()


    #clear = lambda: os.system('cls')
    def start(self):
        text1 = self.text_edit.text()
        if text1 == "":
            try:
                print(text1)
                text1 = self.take_command()

                self.go(text1)
            except sr.UnknownValueError:
                print("error")

        else:
            print(text1)
            self.go(text1)

        # Create a speech recognition object


            # Use the Google Speech Recognition API to transcribe the audio








    def speak(self,text):
        self.transcript_textbox.append(text)
        self.engine.say(text)
        #print(text)
        #print('\n')
        self.text_edit.setText("")

        #print('\n')
        self.engine.runAndWait()


    def greetings(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            str="good morning sir"

        elif hour >= 12 and hour < 16:
            str="good afternoon sir"

        else:
            str="good evening sir"

        self.speak("Iam your voice assistant")
        self.speak(str)





    def name(self):
        self.speak("what should i call you sir")
        username = self.start()
        self.speak('welcome mister')
        self.speak(username)
        columns = shutil.get_terminal_size().columns

        print("#####################".center(columns))
        print("Welcome Mr.", username.center(columns))
        print("#####################".center(columns))

        self.speak("How can i Help you, Sir")


    def take_command(self):
        try:
                with sr.Microphone() as source:
                    self.transcript_textbox.append('listening.....')
                    print('listening')

                    self.listener.adjust_for_ambient_noise(source)
                    #self.listener.pause_threshold = 1
                    voice = self.listener.listen(source,5,3)






        except Exception as z:
            print(z)
            print("say again")
            
        try:
            print('recognising')

            command = self.listener.recognize_google(voice, language='en-in')
            #  command = 'hai'
            command = command.lower()
            self.transcript_textbox.append('recognising...')
            print( command)
            return command


        except Exception as e:
            print(e)
            print("unable to recognize your voice")
            return "none"
            pass








    def qcode(self):
        
        qcode = self.textbox2.text()
        url = pyqrcode.create(qcode)
        url.svg("myqr.svg", scale=8)
        url.png('myqr.png', scale=6)
        url.show()





    def go(self, command):

        if 'play' in command and 'on youtube' in command:
            send = "You -> " + command
            song = command.replace('play', '')
            song = command.replace('on youtube', '')
            self.speak("playing" + song + "on youtube")
            pywhatkit.playonyt(song)
        elif "what's your name" in command or "What is your name" in command:
            self.speak("My friends call me")
            self.speak("My friends call me", self.assname)
            print("My friends call me", self.assname)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print('current time is ' + time)
            self.speak('current time is' + time)
        elif 'who is' in command:
            try:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 2)
               # self.transcript_textbox.append(info)

                self.speak(info)
                print(info)

            except Exception as e:
                print(e)
                #self.transcript_textbox.append(e)


            #self.transcript_textbox.append("My friends call me", self.assname)
        elif 'what is' in command:
            try:
                person = command.replace('what is', '')
                info = wikipedia.summary(person, 2)

                self.speak(info)

            except Exception as e:
                print(e)

        elif 'tell me a joke' in command:
            joke= pyjokes.get_joke()

            self.speak(joke)
        elif 'in wikipedia' in command:
            try:
                self.speak('Searching Wikipedia...')
                command = command.replace("in wikipedia", "")
                results = wikipedia.summary(command, sentences=3)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)
            except Exception as e:
                print(e)

        elif 'search' in command:
            try:
                command=command.replace("search","")
                url = "https://www.google.com.tr/search?q={}".format(command)    
                webbrowser.open(url)
                self.speak("these are results i found")
                self.transcript_textbox.append("these are results i found")
            except Exception as e:
                print(e)

        

        elif 'open youtube' in command:
            self.speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'open google' in command:
            self.speak("Here you go to Google\n")
            webbrowser.open("www.google.com")

        elif 'open stackoverflow' in command:
            self.speak("Here you go to Stack Over flow.Happy coding")
            webbrowser.open("stackoverflow.com")

        elif 'play music' in command or "play song" in command:
            self.speak("Here you go with music")
            # music_dir = "G:\\Song"
            music_dir = "E:\\music"
            songs = os.listdir(music_dir)
            print(songs)
            random = os.startfile(os.path.join(music_dir, songs[1]))

        elif 'the time' in command:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            self.speak(f"Sir, the time is {strTime}")




        elif 'how are you' in command:
            self.speak("I am fine, Thank you")
            self.speak("How are you, Sir")

        elif 'fine' in command or "good" in command:
            self.speak("It's good to know that your fine")

        elif "change my name to" in command:
            command = command.replace("change my name to", "")
            username = command

        elif "change name" in command:
            self.speak("What would you like to call me, Sir ")
            assname = self.start()
            self.speak("Thanks for naming me")



        elif 'exit' in command:
            self.speak("Thanks for giving me your time")
            exit()

        elif "who made you" in command or "who created you" in command:
            self.speak("I have been created by sai and vikram.")

        elif 'joke' in command:
            self.speak(pyjokes.get_joke())
            

        elif "who i am" in command:
            self.speak("If you talk then definitely your human or you are a humanoide robot I think so.")

        elif "why you came to world" in command:
            self.speak("Thanks to sai and vikram. further It's a secret")

        elif 'power point presentation' in command:
            self.speak("opening Power Point presentation")
            power = r"C:\\Users\\GAURAV\\Desktop\\Minor Project\\Presentation\\Voice Assistant.pptx"
            os.startfile(power)

        elif 'tell me about love' in command:
            self.speak("It is 7th sense that destroy all other senses and make person senseless")

        elif "who are you" in command:
            self.speak("I am your virtual assistant created by sai and vikram")

        elif 'reason for you' in command:
            self.speak("I was created as a Minor project by sai and vikram")

        elif 'change background' in command:
            ctypes.windll.user32.SystemParametersInfoW(20,
                                                       0,
                                                       "E:\\my photos\\instagram\\1.png",
                                                       0)
            self.speak("Background changed successfully")

        elif 'open bluestack' in command:
            appli = r"C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe"
            os.startfile(appli)

        elif 'news' in command:

            try:
                from newsapi import NewsApiClient
                import pycountry

                # you have to get your api key from newapi.com and then paste it below
                newsapi = NewsApiClient(api_key='05bf403fddbc48b19540312e87a24ca7')
                self.transcript_textbox.append("enter country name:")
                event_loop = QEventLoop()

                # Connect the clicked signal of the button to the event loop's exit function
                self.button2.clicked.connect(event_loop.quit)

                # Run the event loop until the clicked signal is emitted
                event_loop.exec_()


                # now we will take name of country from user as input

                country=self.textbox2.text()
                input_country = country
                input_countries = [f'{input_country.strip()}']
                countries = {}

                # iterate over all the countries in
                # the world using pycountry module
                for country in pycountry.countries:
                    # and store the unique code of each country
                    # in the dictionary along with it's full name
                    countries[country.name] = country.alpha_2

                # now we will check that the entered country name is
                # valid or invalid using the unique code
                codes = [countries.get(country.title(), 'Unknown code')
                         for country in input_countries]

                # now we have to display all the categories from which user will
                # decide and enter the name of that category
                self.transcript_textbox.append(
                    "Which category are you interested in?\n1.Business\n2.Entertainment\n3.General\n4.Health\n5.Science\n6.Technology\n\nEnter here: ")
                #option = input(
                   # "Which category are you interested in?\n1.Business\n2.Entertainment\n3.General\n4.Health\n5.Science\n6.Technology\n\nEnter here: ")

                event_loop = QEventLoop()
                self.button2.clicked.connect(event_loop.quit)
                event_loop.exec_()
                option = self.textbox2.text()


                # now we will fetch the new according to the choice of the user
                top_headlines = newsapi.get_top_headlines(

                    # getting top headlines from all the news channels
                category=f'{option.lower()}', language='en', country=f'{codes[0].lower()}')

                # fetch the top news inder that category
                Headlines = top_headlines['articles']

                # now we will display the that news with a good readability for user
                if Headlines:
                    for articles in Headlines:
                        b = articles['title'][::-1].index("-")
                        if "news" in (articles['title'][-b + 1:]).lower():
                            print(
                                f"{articles['title'][-b + 1:]}: {articles['title'][:-b - 2]}.")
                            self.transcript_textbox.append(f"{articles['title'][-b + 1:]}: {articles['title'][:-b - 2]}.")
                        else:
                            print(
                                f"{articles['title'][-b + 1:]} News: {articles['title'][:-b - 2]}.")
                            self.transcript_textbox.append( f"{articles['title'][-b + 1:]} News: {articles['title'][:-b - 2]}.")
                else:
                    print(
                        f"Sorry no articles found for {input_country}, Something Wrong!!!")
                self.speak('this are  some latest news i found')
               # option = input("Do you want to search again[Yes/No]?")


            except Exception as e:

                print(str(e))


        elif 'lock window' in command:
            self.speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in command:
            self.speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown / p /f')

        elif 'empty recycle bin' in command:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            self.speak("Recycle Bin Recycled")

        elif "don't listen" in command or "stop listening" in command:
            self.speak("for  5  seconds jarvis stopped from listening commands")
            #a = int(self.start())
            self.time.sleep(5000)
            print(a)

        



        elif "hibernate" in command or "sleep" in command:
            self.speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "log off" in command or "sign out" in command:
            self.speak("Make sure all the application are closed before sign-out")
            self.time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "write a note" in command:
            self.speak("What should i write, sir")
            file = open('E:\\friday.txt', 'a')
            event_loop = QEventLoop()
            self.button2.clicked.connect(event_loop.quit)
            event_loop.exec_()
            note = self.textbox2.text()
           
            strTime = datetime.datetime.now().strftime("%m-%d-%Y %T:%M%p")
            file.write("\n"+strTime)
            file.write(" :- ")
            file.write(note)
            self.speak("data inserted")
    

        elif "show note" in command:
            self.speak("Showing Notes")
            file = open("E:\\friday.txt", "r")
            data=file.read()
            print(data)
            self.transcript_textbox.append(data)
            self.speak(file.read(6))



        # NPPR9-FWDCX-D2C8J-H872K-2YT43
        elif "friday" in command:

            self.greetings()
            self.speak("friday two point o in your service Mister")
            self.speak(self.assname)

        elif "weather" in command:

            # Google Open weather website
            # to get API of Open weather
            api_key = "d05fca532ecda356b983a2ea61350e65"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            self.speak(" City name ")
            print("City name : ")
            event_loop = QEventLoop()
            self.button2.clicked.connect(event_loop.quit)
            event_loop.exec_()
            city_name = self.textbox2.text()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                self.transcript_textbox.append(" Temperature (in kelvin unit) = " + str(
                    current_temperature) + "\n atmospheric pressure (in hPa unit) =" + str(
                    current_pressure) + "\n humidity (in percentage) = " + str(
                    current_humidiy) + "\n description = " + str(weather_description))

            else:
                self.speak(" City Not Found ")

        elif "send message " in command:
            # You need to create an account on Twilio to use this service
            account_sid = 'Account Sid key'
            auth_token = 'Auth token'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=self.start(),
                from_='Sender No',
                to='Receiver No'
            )

            print(message.sid)

        elif "wikipedia" in command:
            webbrowser.open("wikipedia.com")

        elif "Good Morning" in command:
            self.speak("A warm" + command)
            self.speak("How are you Mister")
            self.speak(self.assname)

        # most asked question from google Assistant
        elif "will you be my gf" in command or "will you be my bf" in command:
            self.speak("I'm not sure about, may be you should give me some time")

        elif "how are you" in command:
            self.speak("I'm fine, glad you me that")

        elif 'generate qr code' in command:
            print(command)
            self.speak("enter data in input box")
            event_loop = QEventLoop()
            self.button2.clicked.connect(event_loop.quit)
            event_loop.exec_()
            
            self.qcode()

        elif "navigate to" in command:
            command = command.replace("where is", "")
            command = command.replace("navigate to", "")
            location = command
            self.speak("User asked to Locate")
            self.speak(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location + "")    


        else:
            self.speak("unable to recognize")
            print(command)

try:
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
except Exception as z:
    print(z)