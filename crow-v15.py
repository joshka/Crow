import os
import openai
import re
import sys
import subprocess
import textwrap
import difflib
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

script_name = os.path.basename(__file__)

script_code = open(script_name).read()
instruction = input("What should I do? ")

print(f"Running OpenAI API with instruction: {instruction}")

response = openai.Edit.create(
        model="code-davinci-edit-001",
        input=script_code,
        instruction=instruction,
        temperature=0)
new_script_code = response["choices"][0]["text"]

script_version = int(re.search(r"-v(\d+)\.py", script_name).group(1))
script_name_no_version = script_name.split("-v")[0]
new_script_name = f"{script_name_no_version}-v{script_version + 1}.py"

with open(new_script_name, "w") as f:
    f.write(new_script_code)

# Show the user the new script.
with open(new_script_name) as f:
    new_script_code = f.read()

print(highlight(new_script_code, PythonLexer(), TerminalFormatter()))

# Output information on how to run the new script.
print(f"\nNew script created: {new_script_name}")

# Show the diff between the old script and the new script.
with open(script_name) as f:
    old_script_code = f.readlines()

with open(new_script_name) as f:
    new_script_code = f.readlines()

diff = difflib.unified_diff(old_script_code, new_script_code, fromfile=script_name, tofile=new_script_name)
print("".join(diff))

# Ask the user if they want to commit the new script to git.
commit_to_git = input("Commit to git? [y/n] ")

if commit_to_git == "y":
    # Add the new script to git.
    subprocess.run(["git", "add", new_script_name])

    # Commit the new script to git.
    commit_message = textwrap.fill(f"Generated {new_script_name}\n\n{instruction}", 72)
    subprocess.run(["git", "commit", "-m", commit_message])
