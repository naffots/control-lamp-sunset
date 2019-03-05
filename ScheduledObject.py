from datetime import datetime, timedelta
import urllib.request
from pytz import timezone
from enum import IntEnum
import threading
import time

class Days(IntEnum):
    ALL      = 127 # 1111111
    WEEKDAYS = 31  # 0011111
    WEEKENDS = 96  # 1100000

class ScheduledObject():
    def __init__(self, name, ip, urlOn, urlOff, isDimmable=False):
        self.name = name
        self.ip = ip
        self.urlOn = urlOn
        self.urlOff = urlOff
        self.on_times = []
        self.wake_up_times = []
        self.status = "off"
        self.override = False
        self.brightnessStep = 1
        self.timerstep = 10
        self.isDimmable = isDimmable
        self.timer = None
        self.online = False

    def add_on_time(self, startTime, endTime, days):
        self.on_times.append((startTime, endTime, days))

    def add_wake_up_light_time(self, startTime, endTime, days):
        self.wake_up_times.append((startTime, endTime, days))

    def _get_url(self, url):
        try:
            urllib.request.urlopen(url)
            self.online = True
        except:
            print("{} - Problem with URL ({})".format(self.name, url))
            self.online = False

    def _post_url(self, url, data):
        try:
            params = urllib.parse.urlencode(data)
            params = params.encode('ascii')
            urllib.request.urlopen(url, params)
            self.online = True
        except:
            print("{} - Problem POST URL ({})".format(self.name, url))
            self.online = False

    def get_status(self):
        if self.online:
            return self.status
        else:
            return "off"
        
    def turn_on(self):
        print(" - Turning on!")
        self.status = "on"
        self._get_url("http://" + self.ip + "/" + self.urlOn)

    def turn_off(self):
        print(" - Turning off!")
        self.status = "off"
        self._get_url("http://" + self.ip + "/" + self.urlOff)

    def set_brightness(self, brightness):
        if self.isDimmable:
            self._post_url("http://" + self.ip + "/brightness", {'position':brightness})
        else:
            print("This object do not support brightness")
    
    def get_brightness():
        if self.isDimmable:
            return 100
        else:
            return 100

    def toggle(self):
        self.override = True

        if self.status == "off":
            self.turn_on()
        else:
            self.turn_off()

    def init(self):
        self.turn_off()

    def localize_time(t):
        d = datetime.today()
        return ScheduledObject.localize_date(datetime.combine(d, t))

    def localize_date(d):
        stockholm = timezone('Europe/Stockholm')
        return stockholm.localize(d)

    def update(self):
        print("Updating {}".format(self.name))
        localized_now = ScheduledObject.localize_date(datetime.now())
        day_of_week = datetime.now().weekday()
        day_of_week_mask = 1 << day_of_week

        previousStatus = self.get_status()
        nextStatus = "off"

        # On Off switch
        for (a, b, day) in self.on_times:
            a_date = ScheduledObject.localize_time(a)
            b_date = ScheduledObject.localize_time(b)
            
            if day & day_of_week_mask: 
                if a_date <= localized_now <= b_date:
                    nextStatus = "on"
            
        # Wake up light time
        for (a, b, day) in self.wake_up_times:
            a_date = ScheduledObject.localize_time(a)
            b_date = ScheduledObject.localize_time(b)
            
            if day & day_of_week_mask: 
                if a_date <= localized_now <= b_date:
                    nextStatus = "on"

                    if previousStatus == "off":
                        if not self.timer:
                            self.turn_on()
                            self.set_brightness(0)
                            self.turn_off()
                            self.wake_up_light(self.brightnessStep)
                            time.sleep(2)
                        else:
                            print("Timer is already set for this device")

        if previousStatus == "off" and nextStatus == "on":
            if not self.override:
                self.turn_on()
        elif previousStatus == "on" and nextStatus == "off":
            if not self.override:
                self.turn_off()
        else:
            self.override = False

        


    # Cron job for wake up light
    def wake_up_light(self, brightness):
        if self.status:
            print("{} is increasing brightness to {}".format(self.name, brightness))
            self.set_brightness(brightness) 
            nextBrightness = brightness + self.brightnessStep

            if nextBrightness <= 100:
                # Arm timer width next brightness level
                self.timer = threading.Timer(self.timerstep, self.wake_up_light, args=[nextBrightness])
                self.timer.start()
            else:
                # Unarm timer
                self.timer = None
