"""
1. Read input from the user
2. Send a copy of the currently running script concatenated with the user's instruction to the openai completion api. The returned result will contain a new python script
4. Increment a version number that indicates which version of the script to write.
5. Write the new script to a new file that has the same name as the existing script, but with the new version appended. For example, if this script is called crow-v1.py then the next script will be called crow-v2.py
6. Output the name of the new script and suggest that the user run it with python `name of script`
"""

import requests
import sys
import os

# Get the name of the currently running script
script_name = sys.argv[0]

# Get the user's input
user_input = sys.argv[1]

# Get the current version of the script
version = script_name.split('-')[1].split('.')[0].split('v')[1]

# Get the name of the script without the version number
script_name_no_version = script_name.split('-')[0]

# Get the name of the next version of the script
next_version = str(int(version) + 1)

# Get the name of the next version of the script
next_script_name = script_name_no_version + '-v' + next_version + '.py'

# Get the contents of the currently running script
with open(script_name, 'r') as f:
    script_contents = f.read()

# Concatenate the script contents with the user's input
input_text = script_contents + '\n' + user_input

# Send the input text to the openai completion api
response = requests.post('https://api.openai.com/v1/engines/davinci/completions',
                         json={'prompt': input_text, 'max_tokens': 100, 'temperature': 0.7, 'top_p': 0.9},
                         headers={'Authorization': 'Bearer ' + os.environ['OPENAI_KEY']})

# Get the response text
response_text = response.json()['choices'][0]['text']

# Write the response text to a new file
with open(next_script_name, 'w') as f:
    f.write(response_text)

# Output the name of the new script and suggest that the user run it with python `name of script`
print('Wrote new script to ' + next_script_name)
print('Run it with python ' + next_script_name)