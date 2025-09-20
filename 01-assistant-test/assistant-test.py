from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_core.models import ModelFamily
from autogen_agentchat.messages import TextMessage
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
            "function_calling": False,
            "json_output": False,
            "family": ModelFamily.UNKNOWN,
            "structured_output": False,
        },
        seed = 42,  # seed for caching and reproducibility
        temperature = 0,  # temperature for sampling
        timeout = 400, # timeout,
    )

    assistant = AssistantAgent(
        name = "assistant",
        model_client = custom_model_client,
        description = "A basic first Agent",
    )

    cancellation_token = CancellationToken()

    response = await assistant.on_messages([TextMessage(content="Hello!", source="user")], cancellation_token)
    print(response)

    custom_model_client.close()

asyncio.run(main())