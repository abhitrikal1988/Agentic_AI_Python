import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")

    QA_Engineer= AssistantAgent(name='Abhishek', model_client=openai_model_client,
                               system_message="You are a QA Engineer and need to explain the terms logically")

    Developer = AssistantAgent(name='Ritesh', model_client=openai_model_client,
                              system_message="You are a Developer and can ask any Question about QA Process")

    team =RoundRobinGroupChat(participants=[QA_Engineer,Developer],termination_condition =MaxMessageTermination(max_messages=6))
    await Console(team.run_stream(task="Lets discuss about QA Processes"))
    await openai_model_client.close()


asyncio.run(main())
