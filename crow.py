import os
import difflib
import openai
import subprocess
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import TerminalFormatter

VERSION = "2.0.0"

def edit(script_code, instruction):
    response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=script_code,
            instruction=instruction,
            temperature=0)

    new_script_code = response["choices"][0]["text"]

    return new_script_code

def main():
    script_name = os.path.basename(__file__)
    script_code = open(script_name).read()

    while True:
        instruction = input("Enter an instruction: ")
        new_script_code = edit(script_code, instruction)

        diff = difflib.unified_diff(script_code.splitlines(keepends=True),
                                    new_script_code.splitlines(keepends=True),
                                    fromfile=script_name,
                                    tofile=script_name)
        print(highlight("".join(diff), DiffLexer(), TerminalFormatter()))

        if input("Save changes? [y/N] ").lower() == "y":
            with open(script_name, "w") as f:
                f.write(new_script_code)
            subprocess.run(["git", "commit", "-am", instruction])
            break

if __name__ == "__main__":
    main()
