"""
This script is a simple example of how to use the OpenAI API to generate new
code.

The script takes a single instruction as input, and then uses the OpenAI API
to generate a new script based on the instruction.

The script then shows the diff between the old script and the new script, and
asks the user if they want to commit the new script to git.
"""

import logging
import os
import openai
import re
import sys
import subprocess
import textwrap
import difflib
from pygments import highlight
from pygments.lexers import PythonLexer, DiffLexer
from pygments.formatters import TerminalFormatter

logging.basicConfig(level=logging.INFO)

def call_openai_api(script_code, instruction):
    logging.info(f"Running OpenAI API with instruction: {instruction}")
    response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=script_code,
            instruction=instruction,
            temperature=0.1)
    return response["choices"][0]["text"]

def get_diff(old_script_code, new_script_code, script_name, new_script_name):
    diff = difflib.unified_diff(old_script_code, new_script_code, fromfile=script_name, tofile=new_script_name)
    return highlight("".join(diff), DiffLexer(), TerminalFormatter())

def add_and_commit_script(script_name, instruction):
    # Add the new script to git.
    subprocess.run(["git", "add", script_name])

    # Commit the new script to git.
    commit_title = f"Generated {script_name}"
    commit_message = textwrap.fill(instruction, 72)
    subprocess.run(["git", "commit", "-m", commit_title, "-m", commit_message])

def run_script(script_name):
    # Ask the user if they want to run the new script.
    run_script = input(f"Run {script_name}? [y/n] ")

    if run_script == "y":
        # Run the new script.
        subprocess.run(["python", script_name])
    else:
        # Output the commands to run the new script.
        print(f"\nRun the new script with:\n\npython {script_name}")

def main():
    script_name = os.path.basename(__file__)
    script_code = open(script_name).read()

    crow_version = re.search(r"crow-v(\d+)\.py", script_name).group(1)
    instruction = input(f"Crow v{crow_version}: What should I do? ")

    new_script_code = call_openai_api(script_code, instruction)
    new_script_name = re.sub(r"-v(\d+)\.py", lambda m: f"-v{int(m.group(1)) + 1}.py", script_name)

    with open(new_script_name, "w") as f:
        f.write(new_script_code)

    # Output information on how to run the new script.
    logging.info(f"Created new script: {new_script_name}")

    # Show the diff between the old script and the new script.
    with open(script_name) as f:
        old_script_code = f.readlines()

    with open(new_script_name) as f:
        new_script_code = f.readlines()

    print(get_diff(old_script_code, new_script_code, script_name, new_script_name))

    # Check the code for errors.
    subprocess.run(["python", "-m", "py_compile", new_script_name])

    # Ask the user if they want to commit the new script to git.
    commit_to_git = input("Commit to git? [y/n] ")

    if commit_to_git == "y":
        add_and_commit_script(new_script_name, instruction)

        run_script(new_script_name)

if __name__ == "__main__":
    main()
