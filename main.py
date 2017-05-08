from flask import Flask, render_template, request
from wtforms import Form, BooleanField, StringField, validators, PasswordField
import threading
from datetime import time
from ScheduledObject import ScheduledObject

# Test form with WTForms
class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

# Init
app = Flask(__name__)
form = LoginForm()
scheduleList = {}

wake_time  = time(6,40)
sleep_time = time(22,00)

# Add lamp
s = ScheduledObject("Green Lamp", "192.168.1.68", "on", "off", 0)
s.add_on_time(time(8,0), sleep_time)
scheduleList["green_lamp"] = s

s2 = ScheduledObject("Star map Lamp", "192.168.1.66", "on", "off", 1)
s2.add_on_time(time(20,00), sleep_time)
scheduleList["star_lamp"] = s2

s3 = ScheduledObject("Blinds", "192.168.1.81", "slowOpen", "slowClose", 2)
s3.add_on_time(wake_time, sleep_time)
scheduleList["blinds"] = s3

# Web page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        #scheduleList[index].toggle()
        print("Toggle")

    return render_template("index.html", scheduleList=scheduleList )

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Successful login"

# Init all lamps
def init():
    print("Init lamps")
    for scheduledObject in scheduleList:
        scheduledObject.init()

# Update all lamps
def update():
    for scheduledObject in scheduleList:
        scheduledObject.update()

# Cron job for schedule
def cron_job():
    update()
    t = threading.Timer(60.0, cron_job)
    t.start()

t = threading.Timer(60.0, cron_job)
t.start()
init()
update()

if __name__ == "__main__":
    app.run()
