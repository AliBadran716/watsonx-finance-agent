import gradio as gr
from ai_finance_agent import build_single_agent  # Import the function to build the finance agent

# Build the finance agent once at startup to handle queries efficiently
agent = build_single_agent()

def chat_fn(message, history):
    """
    Handle chat interactions between user and finance agent.
    
    Args:
        message (str): The latest user input message.
        history (list): List of (user, bot) message tuples representing the conversation history.
        
    Returns:
        tuple:
            history (list): Updated conversation history including current turn.
            history (list): Duplicate of updated history for Gradio outputs (chatbot display and latest answer).
    """
    # Initialize history if it is None (first interaction)
    if history is None:
        history = []

    # Send the user message to the finance agent and get the agent's response
    response = agent.invoke({"input": message})
    answer = response.get("output", "⚠️ No response from agent")

    # Append the latest user message and agent answer to the chat history
    history.append((message, answer))

    # Return the updated history twice to update both chatbot and latest answer display
    return history, history


# Create Gradio Blocks interface to build a custom layout with CSS styling
with gr.Blocks(css=".gradio-container {font-family: 'Segoe UI', sans-serif;}") as finance_app:
    # Header description for the app
    gr.Markdown("## 💹 Finance Assistant with Memory\nAsk about stocks, finance news, or general info. The bot remembers context.")

    # Layout with two columns: chat interface and latest response display
    with gr.Row():
        with gr.Column(scale=2):
            # Chatbot component showing conversation history, with fixed height
            chatbot = gr.Chatbot(
                label="💬 Chat History",
                height=500
            )

            # Textbox for user input with placeholder and multiline support
            query = gr.Textbox(
                label="Ask a Question",
                placeholder="e.g. What's the latest news on Apple?",
                lines=2
            )

            # Row for submit and clear buttons
            with gr.Row():
                submit_btn = gr.Button("🚀 Submit", variant="primary")
                clear_btn = gr.Button("🗑️ Clear Chat")

        with gr.Column(scale=1):
            # Textbox to display the latest agent response separately
            response_box = gr.Textbox(
                label="🤖 Latest Answer",
                lines=8,
                placeholder="The bot's last response will appear here..."
            )

    # Define interactions
    # On submit button click: run chat function with user message and conversation history,
    # update chatbot display and latest answer box, and show progress indicator
    submit_btn.click(
        chat_fn,
        inputs=[query, chatbot],
        outputs=[chatbot, response_box],
        show_progress="full"
    )

    # On clear button click: reset chatbot history and latest answer box to empty
    clear_btn.click(
        lambda: ([], ""),
        outputs=[chatbot, response_box]
    )

# Launch the Gradio app on localhost with specified port
finance_app.launch(server_name="127.0.0.1", server_port=7860)