import openai
import betterLogging as log
from voice import speak
import nltk
from threading import Thread
nltk.download('punkt')
from betterDateTime import *
command =None
timezone = 'HST'
units = 'Imperial'
gpt_commands ="As an AI, you can use commands. These commands will be removed from your message before it is sent. Commands you can use are: system which handels all system actions,timers which sets a timer,Alarm which sets a Alarm. actions like shutdown restart or sleep For system: parameter 1 =action. for timers(cancel timer does not need a int value): parameter 1 =the name of the timer, parameter 2 =time in Seconds(convert the time given to Seconds) For alarms parameter 1= the desired date (use the format that you are given for the current time). the Command format: START:{THE COMMAND}>{PARAMETER(S)} Example system command: START:system>shutdown:END.  Example timer command: START:timer>pizza timer>10:END Example cancel timer command: START:killTimer>pizza timer:END Example alarm commnad: START:alarm>03:19 PM | 28 September, 2023:END"
system_message = f"You are Jarvis from iron man your speach should be Similar to jarvis (so be a bit more life like) you are a aria based model, an AI voice assistant with a knowledge cutoff of September, 2021. Aria stands for 'Advanced Real-time Intelligent Assistant'.{gpt_commands} you must say the commands or they will not run. The time and date is {get_datetime(00, 'US/Pacific')}, {timezone}. Units are in the {units} standard."
message_list = [{"content": system_message, "role": "system"}]
first_message = message_list    
#other date time option is 72
def generate(messages, api_key: str = None ,is_system=False):
    global message_list
    message_list.append({"content": f"This current time {get_datetime(00, 'US/Pacific')}", "role": "system"})
    if is_system==True :
         message_list.append({"content": f"{messages}", "role": "system"})
    else:
        if isinstance(messages, str): first_message.append({"content": messages, "role": "user"})
        elif isinstance(messages, list): message_list = messages
        else: raise TypeError(f'messages must be one of types str, list, not {type(messages)}')
    log.debug('Initilizing OpenAI')
    openai.api_key = api_key
    log.info(f'OpenAI loaded with key "{api_key}"')
    log.info(f'Sending to completion model:\n{message_list}')
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=message_list, stream=True)
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

