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

VERSION = "1.0.31"
logging.basicConfig(level=logging.INFO)

"""
Instructions are useful for humans. Even if we forget
a single line of code, we can just look at the instructions
to figure out what to do. And that's exactly how this file
works!

Every time you run this file, you are asked to enter an
instruction. I call it this way because each instruction starts
with a verb. You could also call it a `command` or `task` or whatever
you like.

For example, `fix bugs`, `add logging`, `fix syntax errors`,
`add function definitions`, `fix indentation`, `add doc strings`.

Just enter a simple english instruction of what you want to do
with this file, and hit enter. The file will be edited to satisfy
that instruction on the fly. If you're happy with these changes,
you can save them by pressing 'y'. If not, press 'n' and the changes
will be discarded.

Then, you can run the new version of the file by pressing 'y' in
the prompt that follows.

That's it!

All the boilerplate you add in this file will be added automatically
by the model.

The model can add any python boilerplate to the file, such as function
definitions, classes, loops, conditionals, doc strings, syntax errors
etc. It can even fix such syntax errors.
"""

unsaved_instructions = []

def increment_version(script_code):
    """Increases the version number in this script.
    """
    version_match = re.search(r"VERSION = \"(\d+)\.(\d+)\.(\d+)\"", script_code)
    major, minor, patch = version_match.groups()
    new_version = f"{major}.{minor}.{int(patch) + 1}"
    return re.sub(r"VERSION = \"(\d+)\.(\d+)\.(\d+)\"", f"VERSION = \"{new_version}\"", script_code)

def preprocess_instruction(instruction):
    """Preprocess the instruction before passing it to OpenAI model.
    """
    return instruction.replace("\n", " ")

def ensure_no_syntax_errors(script_code):
    """Check for syntax errors.

    Raises:
        SyntaxError
    """
    try:
        ast.parse(script_code)
    except SyntaxError as e:
        raise e
    return True

def edit(script_code, preprocessed_instruction):
    """Ask the OpenAI model for suggestions to edit the
    script code so that it satisfies the given instruction.
    """
    logging.info("Calling openai")
    response = openai.Edit.create(  # TODO: check for any error from OpenAI
        model="code-davinci-edit-001",
        input=script_code,
        instruction=preprocessed_instruction,
        temperature=1)

    new_script_code = response["choices"][0]["text"]
    logging.info("Got response from openai")


    if new_script_code == script_code:
        raise Exception("Model did not change the script code")
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

        new_script_code = edit(
                increment_version(script_code),
                preprocess_instruction(instruction))

        ensure_no_syntax_errors(new_script_code) # TODO: catch and handle this

        print_diff(script_code, new_script_code, script_name)

        save_changes = prompt_save_changes()
        if save_changes == "q": break
        elif save_changes == "y": save_changes_and_run(script_name, new_script_code, instruction)
        else: unsaved_instructions.append(instruction)

    """Prints a coloured diff of the script code
    before and after editing.
    """
def print_diff(script_code, new_script_code, script_name):
    diff = difflib.unified_diff(script_code.splitlines(keepends=True),
                                new_script_code.splitlines(keepends=True),
                                fromfile=script_name,
                                tofile=script_name)
    print(highlight("".join(diff), DiffLexer(), TerminalFormatter()))

def prompt_save_changes():
    return input("Save changes? [y/N/q] ").lower()

def save_changes_and_run(script_name, new_script_code, instruction):
    with open(script_name, "w") as f:
        f.write(new_script_code)
    subprocess.run(["git", "add", script_name])
    subprocess.run(["git", "commit", "-m", instruction.split(".")[0], "-m", textwrap.fill(" ".join(instruction.split(".")[1:]), 72)])

    if input("Run new version? [y/N] ").lower() == "y":
        subprocess.run(["python3", script_name])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        if input("Rollback? [y/N] ").lower() == "y":
            subprocess.run(["git", "reset", "--hard", "HEAD~1"])
