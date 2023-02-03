"""
1. Read input from the user
2. Send a copy of the currently running script concatenated with the user's instruction to the openai completion api. Use the code-davinci-002 model and assume that the API key is available in the OPENAI_API_KEY environment variable.
3. The returned result should contain a new python script
4. Increment a version number that indicates which version of the script to write.
5. Write the new script to a new file that has the same name as the existing script, but with the new version appended. For example, if this script is called crow-v1.py then the next script will be called crow-v2.py
6. Output the name of the new script and suggest that the user run it with python `name of script`
"""

import os
import sys
import requests
import json

def get_script_name():
    """
    Returns the name of the currently running script
    """
    return os.path.basename(sys.argv[0])

def get_script_version():
    """
    Returns the version number of the currently running script
    """
    return int(get_script_name().split('-')[1].split('.')[0].replace('v', ''))

def get_script_text():
    """
    Returns the text of the currently running script
    """
    with open(get_script_name(), 'r') as f:
        return f.read()

def get_next_script_name():
    """
    Returns the name of the next script
    """
    return get_script_name().replace(f'v{get_script_version()}', f'v{get_script_version() + 1}')

def get_next_script_text(user_input):
    """
    Returns the text of the next script
    """
    api_key = os.environ['OPENAI_API_KEY']
    url = 'https://api.openai.com/v1/engines/davinci/completions'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    data = {
        'prompt': get_script_text() + '\n' + user_input,
        'max_tokens': 100,
        'temperature': 0.7,
        'top_p': 0.9,
        'n': 1,
        'stream': False,
        'logprobs': None,
        'stop': '\n',
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['text']

def write_next_script(text):
    """
    Writes the next script to a file
    """
    with open(get_next_script_name(), 'w') as f:
        f.write(text)

def main():
    """
    The main function
    """
    user_input = input('What should I do next? ')
    next_script_text = get_next_script_text(user_input)
    write_next_script(next_script_text)
    print(f'I wrote a new script called {get_next_script_name()}')
    print(f'You can run it with python {get_next_script_name()}')

if __name__ == '__main__':
    main()