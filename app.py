
import os
import gradio as gr

from game_v1 import chat_v1
from game_v2 import (
    create_initial_state,
    process_action,
    narrate_with_gemini
)


# ==========================================
# APPLICATION SETTINGS
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


INTRODUCTION = """
# AI-Powered Escape Room

Welcome to the mysterious library!

You have awakened inside a locked room.

Your objective is to investigate the environment,
solve puzzles and unlock the exit door.

### Available objects
- Desk
- Bookshelf
- Painting
- Locked drawer
- Exit door

### Instructions
Type natural-language messages into the chat.

Examples:
- Examine the bookshelf.
- Examine the painting.
- Take the key.
- Check inventory.
- Use the key on the drawer.
- Enter 2468 for the drawer.

Good luck escaping!
"""


# ==========================================
# CHAT HANDLER
# ==========================================

def handle_message(message, history, state, version):

    if not message or not message.strip():

        return history, state, "Please enter a message.", ""

    history = history or []

    state = state or create_initial_state()

    if version == "Version 1":

        # Version 1 uses the AI Game Master
        reply = chat_v1(
            message,
            history,
            GEMINI_API_KEY
        )

        # V1 intentionally has weaker validation
        if (
            "7314" in message
            and any(word in message.lower()
                    for word in ["door", "exit", "escape"])
        ):
            state["escaped"] = True

        status = (
            "Version 1 | AI-driven game | "
            + ("Escaped" if state["escaped"] else "Playing")
        )

    else:

        # Version 2 uses Python validation first
        event, state = process_action(
            message,
            state
        )

        # Gemini only narrates the validated event
        reply = narrate_with_gemini(
            event,
            message,
            GEMINI_API_KEY
        )

        status = (
            "Version 2 | Validated game | "
            + ("Escaped" if state["escaped"] else "Playing")
        )

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]

    return history, state, status, ""


# ==========================================
# RESET GAME
# ==========================================

def reset_game():

    return (
        [],
        create_initial_state(),
        "New game started!",
        ""
    )


# ==========================================
# GRADIO INTERFACE
# ==========================================

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="AI-Powered Escape Room"
) as demo:

    gr.Markdown(INTRODUCTION)

    version = gr.Radio(
        choices=["Version 1", "Version 2"],
        value="Version 2",
        label="Select Game Version"
    )

    status = gr.Markdown(
        "Version 2 | Validated game | Playing"
    )

    chatbot = gr.Chatbot(
        label="Game Master",
        type="messages",
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

    send_button.click(
        handle_message,
        inputs=[
            message_box,
            chatbot,
            game_state,
            version
        ],
        outputs=[
            chatbot,
            game_state,
            status,
            message_box
        ]
    )

    message_box.submit(
        handle_message,
        inputs=[
            message_box,
            chatbot,
            game_state,
            version
        ],
        outputs=[
            chatbot,
            game_state,
            status,
            message_box
        ]
    )

    restart_button.click(
        reset_game,
        outputs=[
            chatbot,
            game_state,
            status,
            message_box
        ]
    )


# ==========================================
# LAUNCH APPLICATION
# ==========================================

if __name__ == "__main__":

    demo.launch(
        share=True,
        debug=True
    )
