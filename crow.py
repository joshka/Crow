import os
import difflib
import openai
import subprocess
import logging
import re
import textwrap
import readline
import ast
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import TerminalFormatter

VERSION = "1.0.22"
logging.basicConfig(level=logging.INFO)

unsaved_instructions = []

def increment_version(script_code):
    version_match = re.search(r"VERSION = \"(\d+)\.(\d+)\.(\d+)\"", script_code)
    major, minor, patch = version_match.groups()
    new_version = f"{major}.{minor}.{int(patch) + 1}"
    return re.sub(r"VERSION = \"(\d+)\.(\d+)\.(\d+)\"", f"VERSION = \"{new_version}\"", script_code)

def preprocess_instruction(instruction):
    return instruction.replace("\n", " ")

def ensure_no_syntax_errors(script_code):
    try:
        ast.parse(script_code)
    except SyntaxError as e:
        logging.info("Syntax error")
        return False
    return True

def edit(script_code, preprocessed_instruction):
    logging.info("Calling openai")
    response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=script_code,
            instruction=preprocessed_instruction,
            temperature=0)

    new_script_code = response["choices"][0]["text"]
    logging.info("Got response from openai")

    return new_script_code

    
def main():
    script_name = os.path.basename(__file__)

    def complete(text, state):
        for i, instruction in enumerate(unsaved_instructions):
            if instruction.startswith(text):
                if not state:
                    return instruction
                state -= 1

    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")

    script_code = open(script_name).read()

    while True:
        instruction = input(f"Enter an instruction (v{VERSION}): ").strip()
        if not instruction:
            if unsaved_instructions:
                print("Unsaved instructions:")
                for i, instruction in enumerate(unsaved_instructions):
                    print(f"{i + 1}. {instruction}")
                print()
            continue

        while True:
            new_script_code = edit(increment_version(script_code), preprocess_instruction(instruction))
            if ensure_no_syntax_errors(new_script_code):
                break

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
        else:
            unsaved_instructions.append(instruction)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        if input("Rollback? [y/N] ").lower() == "y":
            subprocess.run(["git", "reset", "--hard", "HEAD~1"])
