# What This Readme is About?

## How to create UV project
- Run this command `uv init --package <custom-project-name>` to create project.

## How to run the Chainlit project using UV
- Run this command for installing chainlit package: `uv add chainlit`.
- Create a file as 'chainbot.py' put that code using decorator.
- Then run this command, `uv run chainlit run ./src/chainlit_uv/chatbot.py`.
- New Screen open after that of chainlit.

## Options to follow (For Knowledge Purpose)
- You can create an env inside a project for separating each environment for standard practicing and avoiding redundant usage of same packages by using.
- For checking the list of env, use `uv venv` command.
- For creating env using `uv venv <env-name>` e.g., `uv venv --python 3.13`
![alt text](image.png)
- For accessing to env, you can use: `.venv\Scripts\activate`, after doing this you can see below image for output:
![alt text](image-1.png)