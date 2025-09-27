import os
import warnings
from dotenv import load_dotenv

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from langchain.memory import ConversationBufferMemory
from langsmith import Client

# Local tools for the agent to use in responses
from tools import SEARCH_TOOL, STOCK_TOOL, NEWS_TOOL

# Suppress deprecation warnings for cleaner output
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Load environment variables from .env file ---
load_dotenv()

def _require(name, v):
    """
    Helper function to ensure an environment variable is set.
    Raises RuntimeError if the variable is missing.
    Args:
        name (str): Name of the environment variable.
        v (str): Value of the environment variable.
    Returns:
        str: The value of the environment variable if present.
    """
    if not v:
        raise RuntimeError(f"Missing env var {name}")
    return v


# Retrieve and validate required environment variables for API connections
API_KEY = _require("WATSONX_API_KEY", os.getenv("WATSONX_API_KEY"))
PROJECT_ID = _require("WATSONX_PROJECT_ID", os.getenv("WATSONX_PROJECT_ID"))
MODEL_ID = _require("WATSONX_MODEL_ID", os.getenv("WATSONX_MODEL_ID"))
URL = _require("WATSONX_URL", os.getenv("WATSONX_URL"))
LANGSMITH_API_KEY = _require("LANGSMITH_API_KEY", os.getenv("LANGSMITH_API_KEY"))

# --- Initialize LangSmith client for prompt management and tracking ---
client = Client(api_key=LANGSMITH_API_KEY)

# --- Configuration parameters for the language model inference ---
parameters = {
    GenParams.MAX_NEW_TOKENS: 512,  # Max tokens generated in response
    GenParams.TEMPERATURE: 0.0,     # Sampling temperature for deterministic output
}

# Credentials dictionary for IBM Watson model API calls
credentials = {"url": URL, "api_key": API_KEY}


def get_watsonx_llm(params=None):
    """
    Creates and returns a WatsonxLLM instance configured with specified parameters.
    Args:
        params (dict, optional): Override default generation parameters.
    Returns:
        WatsonxLLM: Configured language model wrapper for LangChain integration.
    """
    params = params or parameters
    mi = ModelInference(
        model_id=MODEL_ID,
        credentials=credentials,
        params=params,
        project_id=PROJECT_ID,
    )
    return WatsonxLLM(model=mi)


def build_single_agent():
    """
    Builds and configures a LangChain React agent specialized for financial queries.
    Uses multiple tools (search, stock data, news) along with conversation memory
    and a LangSmith-backed prompt template.
    Returns:
        AgentExecutor: An agent executor ready to respond to user input.
    """
    # Instantiate the language model with predefined parameters
    llm = get_watsonx_llm(parameters)

    # Retrieve the custom prompt template stored on LangSmith
    format_prompt = client.pull_prompt("multi-agent-finance-prompt")

    # Set up conversational memory to maintain chat history across turns
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # Define the tools the agent can use to answer queries
    tools = [SEARCH_TOOL, STOCK_TOOL, NEWS_TOOL]

    # Create a React agent that can reason about tool usage and prompts
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=format_prompt,
    )

    # Wrap the agent with memory and tool handling for interactive use
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True  # Print detailed info during execution
    )

    return executor


def main():
    """
    Main entry point for the finance agent CLI.
    Builds the agent and starts an interactive user input loop.
    Users can ask about stocks, finance news, or general information.
    Type 'quit' or 'exit' to stop the program.
    """
    agent = build_single_agent()

    print("🤖 Finance Agent ready! Ask me about stocks, finance news, or general web info.\n")

    # Interactive command loop: process user inputs until exit command
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"quit", "exit"}:
            break

        # Send user input to agent and print its response
        response = agent.invoke({"input": user_input})
        print("Agent:", response["output"])


if __name__ == "__main__":
    main()