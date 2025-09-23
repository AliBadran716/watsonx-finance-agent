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

# Local tools
from tools import SEARCH_TOOL, STOCK_TOOL, NEWS_TOOL

warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Load environment variables ---
load_dotenv()

def _require(name, v):
    if not v:
        raise RuntimeError(f"Missing env var {name}")
    return v

API_KEY = _require("WATSONX_API_KEY", os.getenv("WATSONX_API_KEY"))
PROJECT_ID = _require("WATSONX_PROJECT_ID", os.getenv("WATSONX_PROJECT_ID"))
MODEL_ID = _require("WATSONX_MODEL_ID", os.getenv("WATSONX_MODEL_ID"))
URL = _require("WATSONX_URL", os.getenv("WATSONX_URL"))
LANGSMITH_API_KEY = _require("LANGSMITH_API_KEY", os.getenv("LANGSMITH_API_KEY"))

# --- Connect to LangSmith ---
client = Client(api_key=LANGSMITH_API_KEY)

# --- LLM Config ---
parameters = {
    GenParams.MAX_NEW_TOKENS: 512,
    GenParams.TEMPERATURE: 0.0,
}

credentials = {"url": URL, "api_key": API_KEY}


def get_watsonx_llm(params=None):
    params = params or parameters
    mi = ModelInference(
        model_id=MODEL_ID,
        credentials=credentials,
        params=params,
        project_id=PROJECT_ID,
    )
    return WatsonxLLM(model=mi)


# --- Build a single finance agent ---
def build_single_agent():
    llm = get_watsonx_llm(parameters)

    # Pull your LangSmith prompt template
    format_prompt = client.pull_prompt("multi-agent-finance-prompt")

    # Memory buffer
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # Agent with all tools
    tools = [SEARCH_TOOL, STOCK_TOOL, NEWS_TOOL]

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=format_prompt,
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True
    )

    return executor


def main():
    agent = build_single_agent()

    print("🤖 Finance Agent ready! Ask me about stocks, finance news, or general web info.\n")

    # Interactive loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"quit", "exit"}:
            break

        response = agent.invoke({"input": user_input})
        print("Agent:", response["output"])


if __name__ == "__main__":
    main()
