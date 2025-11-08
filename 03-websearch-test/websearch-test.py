from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.models import ModelFamily
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.base import TaskResult
from dotenv import load_dotenv
import os
import asyncio

async def main() -> None:
    load_dotenv()
    lm_model = os.getenv('LM_MODEL')
    base_url = os.getenv('BASE_URL')

    custom_model_client = OllamaChatCompletionClient(
        model = lm_model, #the name of your running model
        host = base_url, #the local address of the api
        model_info = {
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.UNKNOWN,
            "structured_output": True,
        },
    )

    web_surfer_agent = MultimodalWebSurfer(
        name = "MultimodalWebSurfer",
        model_client = custom_model_client,
        description = "A multimodal agent that can interact with a Chromium-based browser to complete tasks.",
    )

    boss = AssistantAgent(
        name = "organizer",
        model_client = custom_model_client,
        system_message = "You are an organizer. You are in a chat with an agent that can search the Internet." \
        "You must tell the other agent what is the next step that they must take to progress the task given to you." \
        "The web searching agent can't give any feedback to you, only showing what is on the page." \
        "Always give only one step at a time." \
        "The output must be as requested. You cannot search the Internet, and must not attempt to do web searches." \
        "You may only direct the other agent to do web searches.",
        description = "An agent that coordinates the other agents efforts in a group chat to complete tasks.",
        model_client_stream = True,
    )

    agent_team = RoundRobinGroupChat(
        participants = [boss, web_surfer_agent],
        # max_turns = 3,
    )
    # Participantes do chat postam mensagens para todos os outros participantes
    # Rodar comando "playwright install" para instalar navegador baseado em Chromium.

    command = await asyncio.to_thread(input, "Enter command to Web Searcher AI: ")

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(
                task = command,
    )
    await Console(stream)

     # Close the browser controlled by the agent
    await web_surfer_agent.close()
    await custom_model_client.close()

asyncio.run(main())