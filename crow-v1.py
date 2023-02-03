"""
This is a small script called crow-v1.py that writes code that generates new versions of itself. It has a simple algorithm:

1. Read an instruction from the user.
2. Create a text prompt that contains the instruction and a copy of the current script.
3. Call the openai completion api with the prompt, using the model named "code-davinci-002". The openai library sets the API key automatically.
4. Save the output of the completion as a new script with filename version incremented.
"""

import os
import openai
import sys

# openai.api_key = "sk-..."

# Get the current script
script = open(sys.argv[0], "r").read()

# Get the current version number
version = int(script.split("version = ")[1].split("\n")[0])

# Get the next instruction from the user
instruction = input("Instruction: ")

# Create the prompt
prompt = f"{instruction}\n{script}"

# Call the API
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=100,
    temperature=0.9,
    top_p=0.9,
    n=1,
    stream=False,
    logprobs=None,
    stop=["\n"],
)

# Save the output as a new script
new_script = response.choices[0].text
open(f"crow-v{version + 1}.py", "w").write(new_script)
