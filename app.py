
import os
import gradio as gr

from game_v1 import chat_v1
from game_v2 import (
    create_initial_state,
    process_action,
    narrate_with_gemini
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

INTRODUCTION = """
# 🔐 AI-Powered Escape Room

Welcome to the mysterious library!

You have awakened inside a locked room.
Investigate objects, solve puzzles and escape.

### Available objects
- Desk
- Bookshelf
- Painting
- Locked drawer
- Exit door

### Instructions
Try these commands:
- Examine the bookshelf.
- Examine the painting.
- Take the key.
- Check inventory.
- Use the key on the drawer.
- Enter 2468 for drawer.

Good luck!
"""


def handle_message(message, history, state, version):

    if not message or not message.strip():
        return history, state, "Please enter a message.", ""

    history = history or []
    state = state or create_initial_state()

    if version == "Version 1":

        reply = chat_v1(
            message,
            history,
            GEMINI_API_KEY
        )

        status = "Version 1 | AI-driven game"

    else:

        event, state = process_action(
            message,
            state
        )

        reply = narrate_with_gemini(
            event,
            message,
            GEMINI_API_KEY
        )

        status = (
            "Version 2 | Validated game | "
            + ("Escaped!" if state["escaped"] else "Playing")
        )

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]

    return history, state, status, ""


def reset_game():

    return (
        [],
        create_initial_state(),
        "New game started!",
        ""
    )


# Gradio 6 compatible interface
with gr.Blocks(title="AI-Powered Escape Room") as demo:

    gr.Markdown(INTRODUCTION)

    version = gr.Radio(
        choices=["Version 1", "Version 2"],
        value="Version 2",
        label="Select Game Version"
    )

    status = gr.Markdown(
        "Version 2 | Validated game | Playing"
    )

    # Removed type="messages" for compatibility
    chatbot = gr.Chatbot(
        label="Game Master",
        height=430
    )

    game_state = gr.State(
        create_initial_state()
    )

    message_box = gr.Textbox(
        label="Your action",
        placeholder="Examine the bookshelf...",
        lines=2
    )

    with gr.Row():

        send_button = gr.Button(
            "Send Message",
            variant="primary"
        )

        restart_button = gr.Button(
            "Restart Game"
        )

    inputs = [
        message_box,
        chatbot,
        game_state,
        version
    ]

    outputs = [
        chatbot,
        game_state,
        status,
        message_box
    ]

    send_button.click(
        fn=handle_message,
        inputs=inputs,
        outputs=outputs
    )

    message_box.submit(
        fn=handle_message,
        inputs=inputs,
        outputs=outputs
    )

    restart_button.click(
        fn=reset_game,
        outputs=[
            chatbot,
            game_state,
            status,
            message_box
        ]
    )


if __name__ == "__main__":

    demo.launch(
        share=True,
        debug=True,
        theme=gr.themes.Soft()
    )
