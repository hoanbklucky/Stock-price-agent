from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool


from . import prompt
from .triage_agent import triage_agent

# Load the trained model
from google import genai
from google.genai import types

root_agent = Agent(
    model='gemini-2.5-pro',
    name='CareGuideAI_agent',
    description='An agent that predicts triage disposition and notes for clinical plan for tonsillectomy patients.',
    instruction=prompt.VIRTUAL_ASSISTANT_PROMPT,
    tools=[AgentTool(agent=triage_agent)]
)
