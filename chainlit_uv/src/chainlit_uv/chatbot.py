import os
import chainlit as cl

from dotenv import load_dotenv, find_dotenv
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Setup 2: Model
model = OpenAIChatCompletionsModel(
    # model="gemini-2.0-flash",
    # model="gemini-1.5-flash",
    model="gemini-1.5-pro",
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
    instructions="You are a helpful assistant that can answer questions and How can I help you?",
    name="Panaversity Support Agent"
)

# Setup 4: Run
result = Runner.run_sync(
    input="What is the capital of Turkey?",
    run_config=run_config,
    starting_agent=agent1
)

print(result.final_output)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! I'm the Panaversity Support Agent. How can I help you?").send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")

    msg = cl.Message(content="")
    await msg.send()

    #Standard Interface [{"role": "user", "content": "Hello!"}, {...}]
    history.append({"role": "user", "content": message.content})

    # result = await Runner.run(
    #     agent1,
    #     input=history,
    #     run_config=run_config,
    # )

    result = Runner.run_streamed(
    # result = await Runner.run_streamed(
        agent1,
        input=history,
        run_config=run_config,
    )

    # async for event in result.output_stream():
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # print(event.data.delta, end="", flush=True)
            
            # msg.update(event.data.delta)

            # await msg.streamed_chunk(event.data.delta)
            # await msg.stream(event.data.delta)
            await msg.stream_token(event.data.delta)

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    # await cl.Message(
    #     content=result.final_output,
    # ).send()