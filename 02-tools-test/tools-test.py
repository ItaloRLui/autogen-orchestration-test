from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_core.models import ModelFamily
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.tools import AgentTool
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

    web_searcher = AssistantAgent(
        name = "web_searcher",
        model_client = custom_model_client,
        description = "An web searcher agent, for using the web search tool.",
        system_message = "Search for information on the Internet.",
    )
    web_search_tool = AgentTool(agent = web_searcher)

    main_model_client = OpenAIChatCompletionClient(
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
        parallel_tool_calls = False,
    )

    assistant = AssistantAgent(
        name = "assistant",
        model_client = main_model_client,
        tools=[web_search_tool],
        description = "A basic assistant agent.",
        system_message = "You are a helpful assistant.",
    )

    cancellation_token = CancellationToken()

    command = await asyncio.to_thread(input, "Enter command to LLM: ")

    response = await assistant.on_messages([TextMessage(content=command, source="user")], cancellation_token)
    print(response.chat_message.content)

    await custom_model_client.close()

asyncio.run(main())