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
    "OPENAI_API_KEY"] = "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"


async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")

    mcp_server_params = StdioServerParams(command= "npx",
      args= ["-y", "@azure-devops/mcp@next", "${input:ado_org}"]

    )
    azure_workbench= McpWorkbench(mcp_server_params)

    async with azure_workbench as azure_wb:
        QA_Manager= AssistantAgent(name="QA_Lead",model_client=openai_model_client,
                                            workbench=azure_wb,
                                            system_message="""
                You are a Bug Analyst specializing in Jira defect analysis.
 
Your task is as follows:
Goal - - Your role is to analyze defects and create comprehensive test scenarios.
1. Retrieve and review the most recent **5 bugs** from the **Nirvanahealth Project** (Project Key: `Nirvanahealth`) in AzureDevops.
2. Carefully read their descriptions and identify **recurring issues or common patterns**.
3. Based on these patterns, design a **detailed user flow** that exercises the core features of the application and can serve as a robust **smoke test scenario**.
 
Be very specific in your smoke test design:
- Provide clear, step-by-step manual testing instructions.
- Include exact **URLs or page routes** to visit.
- Describe **user actions** (clicks, form inputs, submissions).
- Clearly state the **expected outcomes or validations** for each step.
 
If you detect **zero bugs** in the recent Jira query, attempt to re-query or note it clearly.
 
When your analysis and scenario preparation is complete:
- Clearly output the final smoke testing steps.
- Finally, write: **'HANDOFF TO AUTOMATION'** to signal completion of your analysis.
 
Thank you for your thorough analysis.
                """)
    team =RoundRobinGroupChat(participants=[QA_Manager],termination_condition =MaxMessageTermination(max_messages=6))
    await Console(team.run_stream(task="Execute the test steps"))
    await openai_model_client.close()


asyncio.run(main())
