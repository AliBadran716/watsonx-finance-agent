import gradio as gr
from ai_finance_agent import build_single_agent  # <- import the agent builder from your file

# Build the finance agent once
agent = build_single_agent()

# Chat function for Gradio
def chat_fn(message, history):
    """
    Handle chat interactions with the finance agent.
    Args:
        message (str): User input
        history (list): Previous chat history [(user, bot), ...]
    Returns:
        history (list): Updated chat history
    """
    # Ensure history is initialized
    if history is None:
        history = []

    # Ask the agent
    response = agent.invoke({"input": message})
    answer = response.get("output", "⚠️ No response from agent")

    # Update history
    history.append((message, answer))
    return history, history


with gr.Blocks(css=".gradio-container {font-family: 'Segoe UI', sans-serif;}") as finance_app:
    gr.Markdown("## 💹 Finance Assistant with Memory\nAsk about stocks, finance news, or general info. The bot remembers context.")

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="💬 Chat History",
                height=500
            )

            query = gr.Textbox(
                label="Ask a Question",
                placeholder="e.g. What's the latest news on Apple?",
                lines=2
            )

            with gr.Row():
                submit_btn = gr.Button("🚀 Submit", variant="primary")
                clear_btn = gr.Button("🗑️ Clear Chat")

        with gr.Column(scale=1):
            response_box = gr.Textbox(
                label="🤖 Latest Answer",
                lines=8,
                placeholder="The bot's last response will appear here..."
            )

    # Wire up functionality
    submit_btn.click(
        chat_fn,
        inputs=[query, chatbot],
        outputs=[chatbot, response_box],
        show_progress="full"
    )

    clear_btn.click(
        lambda: ([], ""),
        outputs=[chatbot, response_box]
    )

finance_app.launch(server_name="127.0.0.1", server_port=7860)
