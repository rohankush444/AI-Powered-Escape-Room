
import os
import gradio as gr

from game_v1 import chat_v1
from game_v2 import create_initial_state, process_action

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

WELCOME = """
Welcome to the mysterious library!

You are trapped inside a locked room.
Investigate objects, find clues and escape!
"""


def inventory_text(state):
    items = state.get("inventory", [])

    if not items:
        return "🎒 **Inventory:** Empty"

    return "🎒 **Inventory:** " + ", ".join(items)


def handle_message(message, history, state, version):

    if not message or not message.strip():
        return (
            history,
            state,
            "Please enter an action.",
            "",
            inventory_text(state)
        )

    history = history or []
    state = state or create_initial_state()

    if version == "Version 1":

        reply = chat_v1(
            message,
            history,
            GEMINI_API_KEY
        )

        status = "Version 1 | AI Game Master"

    else:

        # Python validates the action
        event, state = process_action(message, state)

        # No Gemini waiting time in Version 2
        reply = event

        status = (
            "Version 2 | Validated Game | "
            + ("Escaped!" if state["escaped"] else "Playing")
        )

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]

    return (
        history,
        state,
        status,
        "",
        inventory_text(state)
    )


def object_click(obj, history, state, version):

    return handle_message(
        "Examine the " + obj,
        history,
        state,
        version
    )


def restart_game():

    state = create_initial_state()

    history = [
        {"role": "assistant", "content": WELCOME}
    ]

    return (
        history,
        state,
        "New game started!",
        "",
        inventory_text(state)
    )


CSS = """
.gradio-container {
    background: linear-gradient(135deg, #10172b, #202b49);
}
"""


with gr.Blocks(
    title="AI-Powered Escape Room",
    css=CSS
) as demo:

    gr.Markdown("""
    # 🔐 AI-POWERED ESCAPE ROOM
    ### Investigate • Discover • Solve • Escape

    Welcome to the mysterious library.
    Click an object to investigate it!
    """)

    version = gr.Radio(
        choices=["Version 1", "Version 2"],
        value="Version 2",
        label="Select Game Version"
    )

    status = gr.Markdown(
        "Version 2 | Validated Game | Playing"
    )

    with gr.Row():

        with gr.Column(scale=2):

            gr.Markdown("## 🏰 THE MYSTERIOUS LIBRARY")

            gr.HTML("""
            <div style="
                background:linear-gradient(135deg,#493021,#171a29);
                border:2px solid #b68a40;
                border-radius:18px;
                padding:24px;
                color:white;
                text-align:center;
                min-height:180px;
            ">
                <h2 style="color:#f5c76a">
                    Welcome to the Library
                </h2>
                <p style="font-size:45px">📚 🖼️ 🚪</p>
                <p>Investigate the five objects and find your way out!</p>
            </div>
            """)

            gr.Markdown("### 🔎 Investigate an object")

            painting_btn = gr.Button("🖼️ Painting")
            bookshelf_btn = gr.Button("📚 Bookshelf")
            desk_btn = gr.Button("🪑 Desk")
            drawer_btn = gr.Button("🔒 Drawer")
            door_btn = gr.Button("🚪 Exit Door")

            inventory = gr.Markdown(
                "🎒 **Inventory:** Empty"
            )

        with gr.Column(scale=3):

            gr.Markdown("## 🤖 Game Master")

            chatbot = gr.Chatbot(
                value=[
                    {"role": "assistant", "content": WELCOME}
                ],
                label="Your Adventure",
                height=430
            )

            game_state = gr.State(
                create_initial_state()
            )

            message_box = gr.Textbox(
                label="Your action",
                placeholder="Example: Take the key...",
                lines=2
            )

            with gr.Row():

                send_btn = gr.Button(
                    "📨 Send Message",
                    variant="primary"
                )

                restart_btn = gr.Button(
                    "🔄 Restart Game"
                )

    outputs = [
        chatbot,
        game_state,
        status,
        message_box,
        inventory
    ]

    inputs = [
        message_box,
        chatbot,
        game_state,
        version
    ]

    send_btn.click(
        fn=handle_message,
        inputs=inputs,
        outputs=outputs
    )

    message_box.submit(
        fn=handle_message,
        inputs=inputs,
        outputs=outputs
    )

    painting_btn.click(
        fn=lambda h, s, v: object_click(
            "painting", h, s, v
        ),
        inputs=[chatbot, game_state, version],
        outputs=outputs
    )

    bookshelf_btn.click(
        fn=lambda h, s, v: object_click(
            "bookshelf", h, s, v
        ),
        inputs=[chatbot, game_state, version],
        outputs=outputs
    )

    desk_btn.click(
        fn=lambda h, s, v: object_click(
            "desk", h, s, v
        ),
        inputs=[chatbot, game_state, version],
        outputs=outputs
    )

    drawer_btn.click(
        fn=lambda h, s, v: object_click(
            "drawer", h, s, v
        ),
        inputs=[chatbot, game_state, version],
        outputs=outputs
    )

    door_btn.click(
        fn=lambda h, s, v: object_click(
            "door", h, s, v
        ),
        inputs=[chatbot, game_state, version],
        outputs=outputs
    )

    restart_btn.click(
        fn=restart_game,
        inputs=[],
        outputs=outputs
    )


if __name__ == "__main__":

    demo.launch(
        share=True,
        debug=True,
        theme=gr.themes.Soft()
    )
