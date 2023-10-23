import os
import ctypes
import sys
import re
import betterLogging as log
import betterSmartAssist as BST
import threading
import json
from betterDateTime import*

def extract_command_and_parameters(message: str):
    match = re.search(r'START:(.*):END', message)
    if match:  return match.group(1)
    else: return None


def execute_encoded_message(response):
    full_executor = extract_command_and_parameters(response)
    if not full_executor: return response 
    split_executor = full_executor.split(">")
    command = split_executor[0].lower()
    parameters = split_executor[1:]
    if command.lower() == "system":
        command_run = parameters[0]
        if command_run.lower() == "shutdown":
            
            try:
                log.info(r"shutdown ran")
                #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                os.system("shutdown /s /t 1")
            except:
                log.error(r"shutdown throw a error so something happend")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

        if command_run.lower() == "restart":
            
            try:
                #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                os.system("shutdown /r /t 1")
            except:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    if command.lower() == "timer":
        name=(parameters[0])
        time=int(parameters[1])
        timer_thread=threading.Thread(target=BST.TimerClass.setTimer(name,time))
        timer_thread.start()
        return response.replace('START:' + full_executor + ':END', '')
    if command.lower() == "killtimer":
        name=(parameters[0])
        BST.TimerClass.cancelTimer(name)
    if command.lower() == "alarm":BST.AlarmClass.SetAlarm(parameters[0])

#this were the old method for running functions ends and were the new method begins
def DateTime():return get_datetime(00, 'US/Pacific')
functions=[
    {"name": "DateTime",
        "description": "Provides the date and time for you to tell the user",

        "parameters": {
            "type": "object",
            "properties": {},
            
        }
    },
    {
        "name": "system_command",
        "description": "Handle all system actions",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "System action to be performed, e.g. shutdown, restart, sleep"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "timer",
        "description": "Set a timer",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the timer"
                },
                "time": {
                    "type": "string",
                    "description": "Time in seconds it must be a int"
                }
            },
            
            "required": ["name","time"]
        }
    },
    {
        "name": "killTimer",
        "description": "Cancel a timer",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the timer to be cancelled"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "alarm",
        "description": "Set an alarm",
        "parameters": {
            "type": "object",
            "properties": {
                "datetime": {
                    "type": "string",
                    "description": f"The desired date and time for the alarm, in this format example: 03:19 PM | 28 September, 2023(this has to be a actual date it can not be a day like today or a week day). here is the current date and time if needed {DateTime()}"
                }
            },
            "required": ["datetime"]
        }
    }
]

def system_command(action):
    action=action['action']
    if action.lower() == "shutdown":
        
        try:
            print(r"shutdown ran")
            os.system("shutdown /s /t 1")
            print("shutdown")
        except:
            print(r"shutdown throw a error so something happend")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    if action.lower() == "restart":
        
        try:
            os.system("shutdown /r /t 1")
            log.debug("restart")
        except:
            log.error("error with restart")
            #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            action=f"system command {action} ran"
    actions={"action":action}
    return "the system is shuting down tell the user"
