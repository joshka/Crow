# CROW

CROW is an experiment in writing GPT-3 assisted self modifying code. It
basically allows the user to enter an instruction and then apply it to the
current script to run the next time through.

The name CROW comes as a reference to the [RAVEN](https://github.com/daveshap/raven)
project, which has a goal of writing an Artificial General AI (AGI). CROW has
similar goals, but with an underpinning of trying to get CROW to write as much
of itself as possible.

This is my second attempt at CROW (starting at commit 2fe3fbeb1fab7ad617a565ee5ac9c6cc44e1f1b8).
The first attempt was successful, but the script became difficult to refactor
towards neat code (instructing crow to do so). So I figured that I'd start
over instead.

In the initial version of this line, CROW simply prompts for an instruction,
sends it to the openai edit endpoing, and then overwrites the current script
file with the results.

```python
import os
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
with open(script_name, "w") as f:
    f.write(new_script_code)
```

The first few iterations on this have manual commits copying the instruction to
the commit message, while later commits let CROW do this automatically.

```git
2fe3fbe Minimal crow second line
3feaf6f Before saving the new script code show the diff of the existing code
ae8e3a3 Ask for user confirmation before saving
-- missed commit for instruction: After saving commit the file and use the instruction as the commit message
40cb1e5 Use pygments to highlight the diff
45035c6 Add a main method
25f5b95 Refactor the code
85370b8 (HEAD -> crow-v2) Add a version number which is updated before diffing.
```

![CROW Logo - an AI generated image from the prompt: a crow in the style of a terminator from T2, realistic, cgi, movie, posed, 8K, cinematic,](https://cdn.discordapp.com/attachments/1066503804356407346/1071047860637937784/bug_a_crow_in_the_style_of_a_terminator_from_T2_realistic_cgi_m_21b4991c-1e5c-4bf4-ae37-2bbc0a692793.png)