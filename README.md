# 💹 Watsonx Finance Agent

An AI-powered financial assistant that combines **IBM Watsonx**, **LangChain**, and **Gradio** to deliver real-time stock analysis, finance news, and intelligent market insights.  
The agent uses multiple tools (DuckDuckGo, Yahoo Finance, yFinance) with conversational memory, and is accessible via both CLI and a Gradio web app.

---

## 🚀 Features

| Feature                             | Description                                           |
|--------------------------------------|-------------------------------------------------------|
| 🔍 Web search with DuckDuckGo        | Find up-to-date information from the web              |
| 💰 Real-time stock data & recommendations | Powered by yFinance                          |
| 📰 Financial news                    | Get the latest from Yahoo Finance News                |
| 🧠 Conversational memory             | Context-aware chat via LangChain                      |
| 🌐 Interactive Gradio UI             | Seamless chatting in your browser                     |
| 🤝 LangSmith integration             | Prompt management and observability                   |

---

## 📦 Installation

**Clone the repo and install dependencies:**

```bash
git clone https://github.com/your-username/watsonx-finance-agent.git
cd watsonx-finance-agent
pip install -r requirements.txt
```

---

## ⚙️ Environment Setup

Create a `.env` file in the root folder with the following keys:

```env
WATSONX_API_KEY=your_watsonx_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_MODEL_ID=your_model_id
WATSONX_URL=your_watsonx_url
LANGSMITH_API_KEY=your_langsmith_api_key
```

---

## ▶️ Usage

**Run in CLI mode:**
```bash
python ai_finance_agent.py
```

**Run Gradio web app:**
```bash
python app.py
```
This will launch a local app at [http://127.0.0.1:7860](http://127.0.0.1:7860).

---

## 📊 Prompt (LangSmith)

> **The agent uses a structured financial analysis prompt featuring:**

- 🛠️ **Systematic Tool Usage**  
- 📈 **Market, Fundamentals, Technicals & Sentiment Breakdown**  
- 🐻🐂 **Bear / Base / Bull Case Scenarios**  
- 🛡️ **Risk & Recommendation Reporting**  

---

## 🛠️ Tech Stack

| Technology                 | Purpose                                   |
|----------------------------|-------------------------------------------|
| **IBM Watsonx AI**         | Foundation models for financial analysis  |
| **LangChain + LangSmith**  | Prompt management & observability         |
| **yFinance & Yahoo Finance APIs** | Real-time data & news              |
| **DuckDuckGo Search API**  | Web search for up-to-date info            |
| **Gradio**                 | Interactive web UI                        |

---

## 🤝 **Contributing**

✨ PRs and issues are welcome!  
💬 Please open a discussion for major changes before submitting.

---

## 📄 **License**

[MIT License](LICENSE)
