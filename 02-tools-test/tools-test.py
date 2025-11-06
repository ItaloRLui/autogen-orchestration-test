from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
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
        tools = [web_search_mock],
        description = "An agent that uses tools to solve tasks.",
        system_message = "Use tools to solve tasks.",
    )

    cancellation_token = CancellationToken()

    for question in range(1, 3): # Teste com dois comandos seguidos. Dentro de uma mesma sessão, a AI mantém memória das questões.
        # Se a IA identificar que é necessário usar a ferramenta, ela retorna o resultado da função de mock.
        command = await asyncio.to_thread(input, f"Enter command n° {question} to AI: ")

        await Console(assistant.on_messages_stream(messages = [TextMessage(content = command, source = "User")],
                                                   cancellation_token = cancellation_token),
        output_stats = True)

    await custom_model_client.close()

asyncio.run(main())