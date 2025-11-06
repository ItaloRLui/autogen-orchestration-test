from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.models import ModelFamily
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
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
        description = "A multimodal agent that can interact with a Chromium-based browser to complete tasks."
    )

    boss = AssistantAgent(
        name = "organizer",
        model_client = custom_model_client,
        system_message = "Tell the other agents the next steps necessary to complete the given task. The other agents are able" \
        "to use the internet and search for information.",
        description = "An agent that coordinates the other agents efforts in a group chat to complete tasks.",
        model_client_stream = True,
    )

    agent_team = RoundRobinGroupChat(
        participants = [boss, web_surfer_agent],
        name = "Round Robin Web Surfer Group Chat",
        description = "Group chat that the web surfer agent uses",
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