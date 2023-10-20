
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
available_functions = {
    "system_command": c.system_command,
    "DateTime":c.DateTime,
    "timer":BST.TimerClass.setTimer,
    "killTimer":BST.TimerClass.cancelTimer,
    "alarm":BST.AlarmClass.SetAlarm,
    # Add more functions here if needed
}
def gpt_functions(response,messages):

    response_message = response["choices"][0]["message"]

    # Step 1: check if GPT wanted to call a function
    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])

        # Step 2: call the function
        if function_name in available_functions:
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)

            # Step 3: send the info on the function call and function response to GPT
            messages.append(response_message)  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                
            )  # get a new response from GPT where it can see the function response
            return second_response

        return second_response
    else: return response

timezone = 'HST'
units = 'Imperial'
gpt_commands =c.functions
system_message = f"You are Jarvis from iron man your speach should be Similar to jarvis (so be a bit more life like) you are a aria based model, an AI voice assistant with a knowledge cutoff of September, 2021. Aria stands for 'Advanced Real-time Intelligent Assistant'.{gpt_commands} you must say the commands or they will not run. The time and date is {get_datetime(00, 'US/Pacific')}, {timezone}. Units are in the {units} standard."
message_list = [{"content": system_message, "role": "system"}]
first_message = message_list    
def generate(messages, api_key: str = None ):
    global message_list
    if isinstance(messages, str): first_message.append({"content": messages, "role": "user"})
    elif isinstance(messages, list): message_list = messages
    else: raise TypeError(f'messages must be one of types str, list, not {type(messages)}')
    log.debug('Initilizing OpenAI')
    openai.api_key = api_key
    log.info(f'OpenAI loaded with key "{api_key}"')
    log.info(f'Sending to completion model:\n{message_list}')
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo-061', messages=message_list, stream=True,functions=gpt_commands)
    response = gpt_functions(response,messages)
    patritioned_response = ''
    full_response = ''
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']
        if 'content' in chunk_message:
            patritioned_response += chunk_message["content"]
            full_response += chunk_message["content"]
        sentences = nltk.sent_tokenize(patritioned_response)
        if len(sentences) > 1:
            Thread(target=speak, args=[sentences[0]]).start()
            sentences.pop(0)
            patritioned_response = sentences[0]
    if len(nltk.sent_tokenize(full_response)) < 2: 
        Thread(target=speak, args=[full_response]).start()

