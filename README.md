# CROW

CROW is an experiment in the vain of [RAVEN](https://github.com/daveshap/raven).
Where instead of coding up a full architecture, we're just going to let CROW
write itself by kicking it off with a small self editing codebase and then
chatting to it repeatedly.

[Version 1 of crow](crow-v1.py) started (after a bit of trial and error) with
the following code:

```python
import os
import openai
import re
import sys

script_name = os.path.basename(__file__)

script_code = open(script_name).read()
instruction = sys.argv[1]

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
```

The current Version 38 of this code, does a fair bit more. E.g. it shows a colorized diff between versions, adds the code to github, checks the syntax and runs the new code.

Every modification was by instruction to CROW  (check the commit history for details on the instructions). There were a few false steps, that appear in the git history as overwritten commits. (CROW doesn't understand git branching yet).

![CROW Logo - an AI generated image from the prompt: a crow in the style of a terminator from T2, realistic, cgi, movie, posed, 8K, cinematic,](https://cdn.discordapp.com/attachments/1066503804356407346/1071047860637937784/bug_a_crow_in_the_style_of_a_terminator_from_T2_realistic_cgi_m_21b4991c-1e5c-4bf4-ae37-2bbc0a692793.png)