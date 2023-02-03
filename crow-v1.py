"""
This is a small script called crow-v1.py that writes code that generates new versions of itself. It has a simple algorithm:

1. Read an instruction from the user.
2. Create a text prompt that contains the instruction and a copy of the current script.
3. Call the openai completion api with the prompt, and the model parameter set to "code-davinci-002". The api key is stored in an environment variable named OPENAI_API_KEY.
4. Save the output of the completion as a new script with filename version incremented.
5. Output the name of the new script and instructions on how to run it. Do not run the script.
"""

import os
import sys
import json
import requests

def get_script_name():
    return os.path.basename(__file__)

def get_script_version():
    return int(get_script_name().split('-')[-1].split('.')[0])

def get_script_text():
    with open(get_script_name(), 'r') as f:
        return f.read()

def get_prompt(instruction):
    return instruction + '\n' + get_script_text()

def get_completion(prompt):
    url = 'https://api.openai.com/v1/engines/davinci/completions'
    headers = {'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY']}
    data = {'prompt': prompt, 'max_tokens': 100, 'temperature': 0.7, 'top_p': 0.9, 'n': 1, 'stream': False, 'logprobs': None, 'stop': ['\n'], 'frequency_penalty': 0.0, 'presence_penalty': 0.0, 'temperature_bias': 0.0, 'model': 'code-davinci-002'}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['text']

def get_new_script_name():
    return get_script_name().replace(str(get_script_version()), str(get_script_version() + 1))

def write_new_script(script_text):
    with open(get_new_script_name(), 'w') as f:
        f.write(script_text)

def main():
    instruction = input('Enter an instruction: ')
    prompt = get_prompt(instruction)
    completion = get_completion(prompt)
    write_new_script(completion)
    print('New script: ' + get_new_script_name())
    print('Run with: python ' + get_new_script_name())

if __name__ == '__main__':
    main()
