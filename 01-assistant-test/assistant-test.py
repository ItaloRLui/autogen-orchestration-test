from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
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

    assistant = AssistantAgent(
        name = "assistant",
        model_client = custom_model_client,
        description = "A basic first Agent",
        system_message = "You are a helpful assistant.",
    )

    cancellation_token = CancellationToken()

    command = await asyncio.to_thread(input, "Enter command to AI: ")

    response = await assistant.on_messages([TextMessage(content=command, source="user")], cancellation_token)
    print(response.chat_message.content)

    await custom_model_client.close()

asyncio.run(main())