import os
import chainlit as cl

from dotenv import load_dotenv, find_dotenv
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.google.com/v1beta/openai/",
)

# Setup 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Config: Defined at Run Level
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Setup 3: Agent
agent1 = Agent(
    instructions="You are a helpful assistant that can answer questions and",
    name="Panaversity Support Agent"
)

# Setup 4: Run
result = Runner.run_sync(
    input="What is the capital of Turkey?",
    run_config=run_config,
    starting_agent=agent1
)

print(result.final_output)


# @cl.on_message
# async def main(message: cl.Message):
#     # Our custom logic goes here...
#     # Send a fake response back to the user
#     await cl.Message(
#         content=f"Received: {message.content}",
#     ).send()