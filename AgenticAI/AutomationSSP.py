import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams

os.environ[
    "OPENAI_API_KEY"] = ""

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")

    mcp_server_params = StdioServerParams(command="npx",
                                          args=[
                                              "@playwright/mcp@latest"
                                          ]

                                          )
    playwright_workbench = McpWorkbench(mcp_server_params)

    async with playwright_workbench as Playwright_wb:
        automation_engineer = AssistantAgent(name="QA_Engineer", model_client=openai_model_client,
                                             workbench=Playwright_wb,
                                             system_message="You are a Playwright automation expert.Execute the steps as mentioned"
                                                            "Open the URL https://qa1-ids.nirvanahealth.com/applications"
                                                            "Click on Agree button"
                                                            "Wait for few moments until email field appears"
                                                            "Fill email =Abhishek.Agarwal@nirvanahealth.com and click on next button"
                                                            "Wait for few moments until password field appears and Fill  Password = Dharamshala@2025 and click on Signin button"
                                                            "Click on HTA Medical Benefits"
                                                            "Click on Enrollment 2.0"
                                                            "Wait for few moments and click on Health Team Advantage (Medicare) image"
                                                            "Wait for few moments and Click on Member Account tab"
                                                            "Close the browser"

                                                            )
    team = RoundRobinGroupChat(participants=[automation_engineer])
    await Console(team.run_stream(task="Execute the test steps"))
    await openai_model_client.close()


asyncio.run(main())
