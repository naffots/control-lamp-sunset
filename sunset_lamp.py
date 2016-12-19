#!/usr/bin/python3

import sqlite3
from datetime import datetime, time, timedelta
import sys
import os.path
import urllib.request
from astral import Astral, Location
from pytz import timezone
import time as t

def main():

    lightOn = False
    city = Location(('Gothenburg', 'Sweden',
        57.50887, 11.97456, 'Europe/Stockholm', 0))
    stockholm = timezone('Europe/Stockholm')
    
    while (True):
        now = datetime.now()
        d = datetime.today()
        sun = city.sun(date=d, local=True)
        sleep_time = stockholm.localize(datetime.combine(d, time(22,00)))
        wake_time  = stockholm.localize(datetime.combine(d, time( 6,00)))
        work_time  = stockholm.localize(datetime.combine(d, time( 9,00)))
        localized_now = stockholm.localize(now)
        dusk = sun['dusk'] + timedelta(minutes=-30)
        sunrise = sun['sunrise'] + timedelta(minutes=30)
 
        print('Now: %s' % str(localized_now))
        print('Evening: %s -> %s' % (str(dusk), str(sleep_time)))
        print('Morning: %s -> %s' % (str(wake_time), str(sunrise)))

        if dusk <= localized_now <= sleep_time:        
            print ("Evening")
            if not lightOn:
                print ("Turning light on")
                urllib.request.urlopen("http://192.168.1.75/on")
                lightOn = True
        elif wake_time <= localized_now <= sunrise:
            print ("Morning")
            if not lightOn:
                print ("Turning light on")
                urllib.request.urlopen("http://192.168.1.75/on")
                lightOn = True
        else:
            if lightOn:
                print ("Turning light off")
                urllib.request.urlopen("http://192.168.1.75/off")
                lightOn = False

        t.sleep(60)

if __name__ == "__main__":
    sys.exit(main())
