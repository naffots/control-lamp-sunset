from flask import Flask, render_template, request
from wtforms import Form, BooleanField, StringField, validators, PasswordField
import threading
from datetime import datetime, time, timedelta
from astral import Astral, Location
from pytz import timezone
from ScheduledObject import ScheduledObject

# Test form with WTForms
class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

def localize_time(h,m):
    return stockholm.localize(datetime.combine(d, time(h,m)))

# Init
app = Flask(__name__)
form = LoginForm()
scheduleList = []

# ASTRAL
city = Location(('Gothenburg', 'Sweden',
        57.50887, 11.97456, 'Europe/Stockholm', 0))
stockholm = timezone('Europe/Stockholm')
d = datetime.today()
wake_time  = localize_time(6,40)
sleep_time = localize_time(22,00)

# Add lamp
s = ScheduledObject("Green Lamp", "192.168.1.68", "on", "off", 0)
s.add_on_time(localize_time(8,0), sleep_time)
scheduleList.append(s)

s2 = ScheduledObject("Star map Lamp", "192.168.1.66", "on", "off", 1)
s2.add_on_time(localize_time(20,00), sleep_time)
scheduleList.append(s2)

s3 = ScheduledObject("Blinds", "192.168.1.81", "slowOpen", "slowClose", 2)
s3.add_on_time(wake_time, sleep_time)
scheduleList.append(s3)

# Web page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        indexStr = request.form['toggle_lamp']
        index = int(indexStr.replace("Toggle", ""))
        scheduleList[index].toggle()
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
    now = stockholm.localize(datetime.now())
    for scheduledObject in scheduleList:
        scheduledObject.update(now)

# Cron job for schedule
def cron_job():
    update()
    t = threading.Timer(60.0, cron_job)
    t.start()

t = threading.Timer(60.0, cron_job)
t.start()

if __name__ == "__main__":
    init()
    update()
    app.run()
