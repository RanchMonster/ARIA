
import openai
import betterLogging as log
from voice import speak
import nltk
from threading import Thread
nltk.download('punkt')
from betterDateTime import *
import commands as c
import betterSmartAssist as BST
import json
from vars import Name,api_key
import ast
available_functions = {
    "system_command": c.system_command,
    "DateTime":c.DateTime,
    "timer":BST.TimerClass.setTimer,
    "killTimer":BST.TimerClass.cancelTimer,
    "alarm":BST.AlarmClass.SetAlarm,
    # Add more functions here if needed
}
timezone = 'HST'
units = 'Imperial'
gpt_commands =c.functions
system_message = f"Your name is {Name} you are a ARIA based model ARIA stand for advanced real time assistant , an AI voice assistant with a knowledge cutoff of September, 2021. Aria stands for 'Advanced Real-time Intelligent Assistant' The time and date is Units are in the {units} standard.always run the datetime function when asked the time never use the old time"
message_list = [{"content": system_message, "role": "system"}]
first_message = message_list    
def generate(messages, api_key: str = None ,can_run_function=True):
    global message_list
    if isinstance(messages, str): first_message.append({"content": messages, "role": "user"})
    elif isinstance(messages, list): message_list = messages
    else: raise TypeError(f'messages must be one of types str, list, not {type(messages)}')
    log.debug('Initilizing OpenAI')
    openai.api_key = api_key
    log.info(f'OpenAI loaded with key "{api_key}"')
    log.info(f'Sending to completion model:\n{message_list}')
    if can_run_function:response = openai.ChatCompletion.create(model='gpt-3.5-turbo-0613', messages=message_list, stream=True,functions=gpt_commands)
    else:response = openai.ChatCompletion.create(model='gpt-3.5-turbo-0613', messages=message_list, stream=True)
    patritioned_response = ''
    full_response = ''
    function_to_call={ "name": None,"arguments": "",}
    for chunk in response:
        function_call_detected=False
        chunk_message = chunk['choices'][0]['delta']
        if "function_call" in chunk_message:
            function_call_detected = True
            if function_call_detected:
                if "name" in chunk_message["function_call"]:
                        function_to_call["name"] = chunk_message["function_call"]["name"]
                        log.debug(function_to_call)
                        if function_to_call["name"].lower()=="datetime":function_response = f"{c.DateTime()} ";message_list.append({"role": "function","name": function_to_call['name'],"content": function_response,});generate(message_list,api_key,False);break
            if "arguments" in chunk_message["function_call"]:
                #function_to_call[Name] =available_functions[function_to_call["name"]]
                args= chunk_message["function_call"]["arguments"]
                function_to_call["arguments"]+=args
                function_response=None
                #function_response = function_to_call
                if function_response is not None or '': message_list.append({"role": "function","name": function_to_call,"content": function_response,});generate(message_list,api_key,False);break
        elif 'content' in chunk_message and not function_call_detected:
            patritioned_response += chunk_message["content"]
            full_response += chunk_message["content"]
        sentences = nltk.sent_tokenize(patritioned_response)
        if len(sentences) > 1:
            Thread(target=speak, args=[sentences[0]]).start()
            sentences.pop(0)
            patritioned_response = sentences[0]
    if len(nltk.sent_tokenize(full_response)) < 2 and not function_call_detected: Thread(target=speak, args=[full_response]).start()

    if function_to_call["name"]is not None:
        function=function_to_call["name"]
        function_to_call["name"] =available_functions[function_to_call["name"]]
        if function=='timer':Thread(target=BST.TimerClass.setTimer,args=[function_to_call["arguments"]]).start();function_response='timer is set'
        else:
            function_response=function_to_call['name'](function_to_call['arguments'])
            if function_response is not None or '': message_list.append({"role": "function","name": function,"content": function_response,});generate(message_list,api_key,False)

