import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")

    assistant = AssistantAgent(name='Abhishek', model_client=openai_model_client)
    image = Image.from_file("C:/Users/Abhishek.Agarwal/Desktop/Abhi_Photo.jpg")

    multimodal_message = MultiModalMessage(content=["What do you see in this image?", image],source="user")
    await Console(assistant.run_stream(task=multimodal_message))
    await openai_model_client.close()


asyncio.run(main())
