import os
import ctypes
import sys
import re
import betterLogging as log
import betterSmartAssist as BST
import threading
def extract_command_and_parameters(message: str):
    match = re.search(r'START:(.*):END', message)
    if match:  return match.group(1)
    else: return None
import json

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

"""
functions=[
    {"name": "DateTime",
        "description": "Provides the date and time for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "int",
                    "description": "the format you want "
                }
            },
            "required": ["action"]
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
                    "type": "number",
                    "description": "Time in seconds"
                }
            },
            "required": ["name", "time"]
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
                    "description": "The desired date and time for the alarm, e.g. 03:19 PM | 28 September, 2023"
                }
            },
            "required": ["datetime"]
        }
    }
]

def system_command(action:str):
    if action.lower() == "shutdown":
        
        try:
            log.info(r"shutdown ran")
            #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            #os.system("shutdown /s /t 1")
            print("shutdown")
        except:
            log.error(r"shutdown throw a error so something happend")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    if action.lower() == "restart":
        
        try:
            #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            #os.system("shutdown /r /t 1")
            log.error("restart")
        except:
            log.error("error with restart")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            actions={
                "what_happend":f"system command {action} ran"
            }
    return json.dump(actions)
"""