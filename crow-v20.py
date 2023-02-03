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

def get_script_name():
    return os.path.basename(__file__)

def get_script_code(script_name):
    return open(script_name).read()

def get_crow_version(script_name):
    return re.search(r"crow-v(\d+)\.py", script_name).group(1)

def get_instruction(crow_version):
    return input(f"Crow v{crow_version}: What should I do? ")

def get_new_script_code(script_code, instruction):
    print(f"Running OpenAI API with instruction: {instruction}")

    response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=script_code,
            instruction=instruction,
            temperature=0)
    return response["choices"][0]["text"]

def get_new_script_name(script_name):
    script_version = int(re.search(r"-v(\d+)\.py", script_name).group(1))
    script_name_no_version = script_name.split("-v")[0]
    return f"{script_name_no_version}-v{script_version + 1}.py"

def write_new_script(new_script_name, new_script_code):
    with open(new_script_name, "w") as f:
        f.write(new_script_code)

def get_old_script_code(script_name):
    with open(script_name) as f:
        return f.readlines()

def get_new_script_code(new_script_name):
    with open(new_script_name) as f:
        return f.readlines()

def get_diff(old_script_code, new_script_code, script_name, new_script_name):
    return difflib.unified_diff(old_script_code, new_script_code, fromfile=script_name, tofile=new_script_name)

def commit_to_git(new_script_name, instruction):
    # Add the new script to git.
    subprocess.run(["git", "add", new_script_name])

    # Commit the new script to git.
    commit_message = textwrap.fill(f"Generated {new_script_name}\n\n{instruction}", 72)
    subprocess.run(["git", "commit", "-m", commit_message])

script_name = get_script_name()
script_code = get_script_code(script_name)
crow_version = get_crow_version(script_name)
instruction = get_instruction(crow_version)
new_script_code = get_new_script_code(script_code, instruction)
new_script_name = get_new_script_name(script_name)
write_new_script(new_script_name, new_script_code)

# Output information on how to run the new script.
print(f"\nNew script created: {new_script_name}")

# Show the diff between the old script and the new script.
old_script_code = get_old_script_code(script_name)
new_script_code = get_new_script_code(new_script_name)
diff = get_diff(old_script_code, new_script_code, script_name, new_script_name)
print(highlight("".join(diff), DiffLexer(), TerminalFormatter()))

# Ask the user if they want to commit the new script to git.
commit_to_git = input("Commit to git? [y/n] ")

if commit_to_git == "y":
    commit_to_git(new_script_name, instruction)

    # Ask the user if they want to run the new script.
    run_script = input("Run script? [y/n] ")

    if run_script == "y":
        # Run the new script.
        subprocess.run(["python", new_script_name])
    else:
        # Output the commands to run the new script.
        print(f"\nRun the new script with:\n\npython {new_script_name}")
