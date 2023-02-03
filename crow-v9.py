import os
import openai
import re
import sys
import subprocess

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
subprocess.run(["pygmentize", new_script_name])

# Output information on how to run the new script.
print(f"New script created: {new_script_name}")
print(f"Run the new script with: python {new_script_name}")

# Show the diff between the old script and the new script.
subprocess.run(["diff", script_name, new_script_name])

# Ask the user if they want to commit the new script to git.
commit_to_git = input("Commit to git? [y/n] ")

if commit_to_git == "y":
    # Add the new script to git.
    subprocess.run(["git", "add", new_script_name])

    # Commit the new script to git.
    subprocess.run(["git", "commit", "-m", f"Generated {new_script_name}\n\n{instruction}"])
