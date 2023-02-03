"""
This is a small script called crow that writes code that generates new versions of itself.

1. Read an instruction from the user via the console input.
2. Make a prompt that is the instruction followed by the contents of the currently running script.
2. Send the prompt to the openai completion api. Use the code-davinci-002 model.
3. The returned result will contain a new python script.
4. Increment a version number that indicates which version of the script to write.
5. Write the new script to a new file that has the same name as the existing script, but with the new version appended. For example, if this script is called crow-v1.py then the next script will be called crow-v2.py
6. Output the name of the new script and suggest that the user run it with python `name of script`

The OpenAI API for completions is available using the openai pypi library here is an example of the code to call it:

import openai
openai.Completion.create(model="code-davinci-002", prompt="Say this is a test")`
"""

import openai
import sys
import os

def get_next_version(filename):
    """
    Given a filename, return the next version number.
    """
    # Get the current version number
    version = int(filename.split("-v")[1].split(".py")[0])
    # Increment the version number
    version += 1
    # Return the new version number
    return version

def get_new_filename(filename):
    """
    Given a filename, return the next version of the filename.
    """
    # Get the current version number
    version = get_next_version(filename)
    # Return the new filename
    return filename.split("-v")[0] + "-v" + str(version) + ".py"

def get_prompt(filename, instruction):
    """
    Given a filename and an instruction, return the prompt to send to the openai api.
    """
    # Read the contents of the file
    with open(filename, "r") as f:
        contents = f.read()
    # Return the prompt
    return instruction + "\n" + contents

def get_completion(prompt):
    """
    Given a prompt, return the completion from the openai api.
    """
    # Call the openai api
    completion = openai.Completion.create(model="code-davinci-002", prompt=prompt)
    # Return the completion
    return completion

def write_completion(filename, completion):
    """
    Given a filename and a completion, write the completion to the filename.
    """
    # Write the completion to the filename
    with open(filename, "w") as f:
        f.write(completion)

def main():
    """
    This is the main function.
    """
    # Get the filename of this script
    filename = sys.argv[0]
    # Get the instruction from the user
    instruction = input("Enter an instruction: ")
    # Get the prompt
    prompt = get_prompt(filename, instruction)
    # Get the completion
    completion = get_completion(prompt)
    # Get the new filename
    new_filename = get_new_filename(filename)
    # Write the completion to the new filename
    write_completion(new_filename, completion)
    # Print the new filename
    print("Wrote new script to " + new_filename)
    # Print the command to run the new script
    print("Run it with python " + new_filename)

if __name__ == "__main__":
    main()
