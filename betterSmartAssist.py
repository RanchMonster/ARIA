import time
import threading
import betterDateTime as BDT
import os
from dotenv import load_dotenv
import voice as voice
import BetterListManager as lm
import datetime
import time as t
import ast
load_dotenv()
def env(s: str): return os.environ.get(s)
api_key = env('api_key')

class TimerClass:
   
    def timer(seconds):
        end_time = time.time() + seconds
        while time.time() < end_time:pass
        return True

    def setTimer(dict):
        dict=ast.literal_eval(dict)
        seconds=dict['time']
        name=dict['name']
        seconds=int(seconds)
        timer_thread = threading.Thread(target=TimerClass.timer, args=[seconds])
        timer_thread.start()
        lm.add_item('Timers',name)
        while timer_thread.is_alive(): pass
        timers=lm.get_list('Timers')
        for timer_name in timers:
            if timer_name == name:
                lm.remove_item('Timers',name)
                voice.speak(f"{name} is done ")

    def cancelTimer(dict): 
        dict=ast.literal_eval(dict)
        name=name['name']
        lm.remove_item('Timers',name)

class AlarmClass:
    def AlarmSys():
        while True:
            Alarms=lm.get_list("Alarms")
            for Alarm in Alarms:
                time=BDT.get_datetime(00,'US/Pacific')
                if time == Alarm:lm.remove_item("Alarms",Alarm); print('it works you dumb')
                else:pass
            t.sleep(0.1)

    def SetAlarm(time:str):
        time=ast.literal_eval(time)
        time=time["datetime"]
        lm.add_item('Alarms',time);return 'alarm is set'
    def cancelAlarm(time:str):lm.remove_item('Alarms',time)

