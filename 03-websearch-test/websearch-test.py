from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import os
import asyncio

async def main() -> None:
    load_dotenv()
    lm_model = os.getenv('LM_MODEL')
    base_url = os.getenv('BASE_URL')
    api_key  = os.getenv('API_KEY')

    custom_model_client = OpenAIChatCompletionClient(
        model = lm_model, #the name of your running model
        base_url = base_url, #the local address of the api
        api_key = api_key, # just a placeholder
        model_info = {
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.O3,
            "structured_output": True,
        },
        seed = 42,  # seed for caching and reproducibility
        temperature = 0,  # temperature for sampling
        timeout = 400, # timeout,
    )

    web_surfer_agent = MultimodalWebSurfer(
        name = "MultimodalWebSurfer",
        model_client = custom_model_client,
        description = "A multimodal agent that can interact with a Chromium-based browser to complete tasks."
    )

    agent_team = RoundRobinGroupChat(
        participants = [web_surfer_agent],
        name = "Round Robin Web Surfer Group Chat",
        description = "Group chat that the web surfer agent uses",
        max_turns = 3,
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