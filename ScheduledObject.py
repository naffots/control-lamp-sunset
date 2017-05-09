from datetime import datetime, time, timedelta
import urllib.request
from astral import Astral, Location
from pytz import timezone

class ScheduledObject():
    def __init__(self, name, ip, urlOn, urlOff):
        self.name = name
        self.ip = ip
        self.urlOn = urlOn
        self.urlOff = urlOff
        self.on_times = []
        self.status = "off"
        self.override = False

    def add_on_time(self, startTime, endTime):
        self.on_times.append((startTime, endTime))

    def _get_url(self, url):
        try:
            urllib.request.urlopen(url)
        except:
            print("Problem with URL ({})".format(url))

    def turn_on(self):
        self.status = "on"
        self._get_url("http://" + self.ip + "/" + self.urlOn)

    def turn_off(self):
        self.status = "off"
        self._get_url("http://" + self.ip + "/" + self.urlOff)

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

        previousStatus = self.status
        nextStatus = "off"

        for (a, b) in self.on_times:
            a_date = ScheduledObject.localize_time(a)
            b_date = ScheduledObject.localize_time(b)

            if a_date <= localized_now <= b_date:
                nextStatus = "on"
        
        if previousStatus == "off" and nextStatus == "on":
            if not self.override:
                print(" - Turning on!")
                self.turn_on()
        elif previousStatus == "on" and nextStatus == "off":
            if not self.override:
                print(" - Turning off!")
                self.turn_off()
        else:
            self.override = False


