from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_core.models import ModelFamily
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import os
import asyncio

def web_search_mock(query: str) -> str:
    """Find information on the web"""
    return "The Labrador Retriever or simply Labrador is a British breed of retriever gun dog. "

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

    assistant = AssistantAgent(
        name = "assistant",
        model_client = custom_model_client,
        tools = [web_search_mock],
        description = "An agent that uses tools to solve tasks.",
        system_message = "Use tools to solve tasks.",
    )

    cancellation_token = CancellationToken()

    for question in range(1, 3): # Teste com dois comandos seguidos. Dentro de uma mesma sessão, a AI mantém memória das questões.

        command = await asyncio.to_thread(input, f"Enter command n° {question} to AI: ")

        await Console(assistant.on_messages_stream(messages = [TextMessage(content = command, source = "User")],
                                                   cancellation_token = cancellation_token),
        output_stats = True)

    await custom_model_client.close()

asyncio.run(main())