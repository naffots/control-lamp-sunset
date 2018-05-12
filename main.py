from flask import Flask, render_template, request, redirect
from wtforms import Form, BooleanField, StringField, validators, PasswordField
import threading
from datetime import time
from ScheduledObject import ScheduledObject, Days
from ScheduledTplink import ScheduledTplink
import json

# Init
app = Flask(__name__)
scheduleList = {}

wake_time  = time(6,20)
sleep_time = time(22,00)

# Add lamp
s = ScheduledObject("Green Lamp", "192.168.1.64", "on", "off")
s.add_on_time(time(8,0), sleep_time, Days.ALL)
scheduleList["green_lamp"] = s

s2 = ScheduledObject("Star map Lamp", "192.168.1.66", "on", "off")
s2.add_on_time(time(20,00), time(23,00), Days.ALL)
scheduleList["star_lamp"] = s2

s3 = ScheduledObject("Blinds", "192.168.1.81", "open", "close", isDimmable=True)
s3.add_wake_up_light_time(wake_time, sleep_time, Days.WEEKDAYS)
s3.add_wake_up_light_time(time(9,20), sleep_time, Days.WEEKENDS)
scheduleList["blinds"] = s3

s4 = ScheduledTplink("Batcave", "192.168.1.70", "bulb", isDimmable=True)
s4.add_on_time(time(19,00), sleep_time, Days.ALL)
s4.add_wake_up_light_time(wake_time, time(9,00), Days.WEEKDAYS)
s4.add_wake_up_light_time(time(9,20), time(11,0), Days.WEEKENDS)
scheduleList["batcave"] = s4

s5 = ScheduledTplink("Ljusslinga", "192.168.1.88", "plug")
s5.add_on_time(time(7, 00), time(10,00), Days.ALL)
s5.add_on_time(time(18,00), sleep_time, Days.ALL)
scheduleList["ljusslinga"] = s5

s6 = ScheduledObject("LED-slinga", "192.168.1.84", "on", "off", isDimmable=True)
s6.add_on_time(wake_time, sleep_time, Days.WEEKDAYS)
s6.add_on_time(time(9,20), sleep_time, Days.WEEKENDS)
scheduleList["ledstrip"] = s6

s7 = ScheduledObject("TV", "192.168.1.73", "on", "off")
scheduleList["tv"] = s7

# Web page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        schedName = request.form["name"]
        print(schedName)

        if request.form["action"] == "toggle":
            scheduleList[schedName].toggle()
        elif request.form["action"] == "edit":
            print("User pressed edit {}".format(schedName))
        return redirect("/", code=303)

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


def main():
    t = threading.Timer(60.0, cron_job)
    t.start()
    init()
    update()
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
