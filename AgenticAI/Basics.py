import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = "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"


async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")
    assistant = AssistantAgent(name='Abhishek', model_client=openai_model_client)
    await Console(assistant.run_stream(task="What is the 222*34?"))
    await openai_model_client.close()


asyncio.run(main())
