import os
import openai
import re
import sys

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

# Output information on how to run the new script.
print(f"New script created: {new_script_name}")
print(f"Run the new script with: python {new_script_name} <instruction>")