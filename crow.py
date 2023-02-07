import os
import difflib
import openai
import subprocess
import logging
import re
import textwrap
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import TerminalFormatter

VERSION = "1.0.15"
logging.basicConfig(level=logging.INFO)

def increment_version(script_code):
    version_match = re.search(r"VERSION = \"(\d+)\.(\d+)\.(\d+)\"", script_code)
    major, minor, patch = version_match.groups()
    new_version = f"{major}.{minor}.{int(patch) + 1}"
    return re.sub(r"VERSION = \"(\d+)\.(\d+)\.(\d+)\"", f"VERSION = \"{new_version}\"", script_code)

def edit(script_code, instruction):
    logging.info("Calling openai")
    response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=script_code,
            instruction=instruction,
            temperature=0)

    new_script_code = response["choices"][0]["text"]
    logging.info("Got response from openai")

    return new_script_code

    
def main():
    script_name = os.path.basename(__file__)
    script_code = open(script_name).read()

    while True:
        instruction = input(f"Enter an instruction (v{VERSION}): ")
        new_script_code = edit(increment_version(script_code), instruction)

        diff = difflib.unified_diff(script_code.splitlines(keepends=True),
                                    new_script_code.splitlines(keepends=True),
                                    fromfile=script_name,
                                    tofile=script_name)
        print(highlight("".join(diff), DiffLexer(), TerminalFormatter()))

        save_changes = input("Save changes? [y/N/q] ").lower()
        if save_changes == "q":
            break
        elif save_changes == "y":
            with open(script_name, "w") as f:
                f.write(new_script_code)
            subprocess.run(["git", "add", script_name])
            subprocess.run(["git", "commit", "-m", instruction.split(".")[0], "-m", textwrap.fill(instruction, 72)])

            if input("Run new version? [y/N] ").lower() == "y":
                subprocess.run(["python3", script_name])
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        if input("Rollback? [y/N] ").lower() == "y":
            subprocess.run(["git", "reset", "--hard", "HEAD~1"])
