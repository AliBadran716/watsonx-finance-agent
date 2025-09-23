# 💹 Watsonx Finance Agent

An AI-powered financial assistant that combines **IBM Watsonx**, **LangChain**, and **Gradio** to deliver real-time stock analysis, finance news, and intelligent market insights.  
The agent uses multiple tools (DuckDuckGo, Yahoo Finance, yFinance) with conversational memory, and is accessible via both CLI and a Gradio web app.

---

## 🚀 Features
- 🔍 Web search with DuckDuckGo  
- 💰 Real-time stock data & recommendations with yFinance  
- 📰 Financial news with Yahoo Finance News  
- 🧠 Conversational memory powered by LangChain  
- 🌐 Interactive Gradio UI for seamless chatting  
- 🤝 LangSmith integration for prompt management and observability  

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/your-username/watsonx-finance-agent.git
cd watsonx-finance-agent
pip install -r requirements.txt
```
## ⚙️ Environment Setup
Create a .env file in the root folder with the following keys:

```env
WATSONX_API_KEY=your_watsonx_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_MODEL_ID=your_model_id
WATSONX_URL=your_watsonx_url
LANGSMITH_API_KEY=your_langsmith_api_key
```
## ▶️ Usage
Run in CLI mode:
```bash
python ai_finance_agent.py
```
Run Gradio web app:
```bash
python app.py
```
This will launch a local app at http://127.0.0.1:7860.

## 📊 Prompt (LangSmith)
The agent uses a structured financial analysis prompt with:

Systematic tool usage

Market, fundamentals, technicals, and sentiment breakdown

Bear/Base/Bull case scenarios

Risk & recommendation reporting

## 🛠️ Tech Stack
IBM Watsonx AI (foundation models)

LangChain + LangSmith

yFinance & Yahoo Finance APIs

DuckDuckGo Search API

Gradio for UI

## 🤝 Contributing
PRs and issues are welcome! Please open a discussion for major changes before submitting.

## 📄 License
MIT License
