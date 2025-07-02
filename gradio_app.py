import gradio as gr
from app import ask_question  # Função já integrada com retriever + LLM

# Chat logic
def qa_interface(question, chat_history):
    if question.strip().lower() in ["exit", "quit"]:
        return "", chat_history + [("exit", "Session ended.")]
    
    try:
        answer = ask_question(question)
    except Exception as e:
        answer = f"⚠️ Error: {str(e)}"
    
    chat_history.append((question, answer))
    return "", chat_history

# UI
with gr.Blocks() as demo:
    gr.Markdown("# Compliance Q&A Assistant")
    gr.Markdown(
        "Ask questions related to compliance documents. This prototype uses a local LLM + vector search."
    )

    chatbot = gr.Chatbot(label="Chat History", height=400)
    
    with gr.Row():
        msg = gr.Textbox(
            label="Your Question",
            placeholder="e.g. Has Tesla ever appeared in OFAC sanctions?",
            scale=4
        )
        submit = gr.Button("Ask", scale=1)

    submit.click(fn=qa_interface, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch()
