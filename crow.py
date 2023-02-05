import os
import difflib
import openai

instruction = input("Enter an instruction: ")

script_name = os.path.basename(__file__)
script_code = open(script_name).read()
response = openai.Edit.create(
        model="code-davinci-edit-001",
        input=script_code,
        instruction=instruction,
        temperature=0)

new_script_code = response["choices"][0]["text"]

diff = difflib.unified_diff(script_code.splitlines(keepends=True),
                            new_script_code.splitlines(keepends=True),
                            fromfile=script_name,
                            tofile=script_name)
print("".join(diff))

if input("Save changes? [y/N] ").lower() == "y":
    with open(script_name, "w") as f:
        f.write(new_script_code)
