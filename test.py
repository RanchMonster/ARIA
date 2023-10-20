import openai
import json
import commands as c
import betterSmartAssist as BST
import re
import gen_stream as g
# Define available functions
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

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])

        # Step 3: call the function
        if function_name in available_functions:
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)

            # Step 4: send the info on the function call and function response to GPT
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


