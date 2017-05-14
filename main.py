from flask import Flask, render_template, request
from wtforms import Form, BooleanField, StringField, validators, PasswordField
import threading
from datetime import time
from ScheduledObject import ScheduledObject, Days

# Init
app = Flask(__name__)
scheduleList = {}

wake_time  = time(6,40)
sleep_time = time(22,00)

# Add lamp
s = ScheduledObject("Green Lamp", "192.168.1.68", "on", "off")
s.add_on_time(time(8,0), sleep_time, Days.ALL)
scheduleList["green_lamp"] = s

s2 = ScheduledObject("Star map Lamp", "192.168.1.66", "on", "off")
s2.add_on_time(time(20,00), time(23,00), Days.ALL)
scheduleList["star_lamp"] = s2

s3 = ScheduledObject("Blinds", "192.168.1.81", "slowOpen", "slowClose")
s3.add_on_time(wake_time, sleep_time, Days.WEEKDAYS)
s3.add_on_time(time(9,40), sleep_time, Days.WEEKENDS)
scheduleList["blinds"] = s3

# Web page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        schedName = request.form["name"]

        if request.form["action"] == "toggle":
            scheduleList[schedName].toggle()
        elif request.form["action"] == "edit":
            print("User pressed edit {}".format(schedName))

    sortedList = sorted(scheduleList.items(), key= lambda x: x[1].name)
    return render_template("index.html", scheduleList=sortedList )

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    schedObject = scheduleList[request.args.get("name")]
    return render_template("edit.html", scheduleObject = schedObject)

# Init all lamps
def init():
    print("Init lamps")
    for (key, scheduledObject) in scheduleList.items():
        scheduledObject.init()

# Update all lamps
def update():
    for (key, scheduledObject) in scheduleList.items():
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
