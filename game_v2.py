
import re
from google import genai


# ==========================================
# 1. GAME CONFIGURATION
# ==========================================

OBJECTS = [
    "desk",
    "bookshelf",
    "painting",
    "drawer",
    "door"
]

DRAWER_CODE = "2468"
FINAL_DOOR_CODE = "7314"


# ==========================================
# 2. INITIAL GAME STATE
# ==========================================

def create_initial_state():

    return {
        "examined": [],
        "inventory": [],
        "key_available": False,
        "key_used": False,
        "bookshelf_clue_seen": False,
        "drawer_open": False,
        "note_read": False,
        "door_open": False,
        "escaped": False,
        "solved_puzzles": [],
        "actions": []
    }


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def record_action(state, action):

    state["actions"].append(action)

    return state


def add_puzzle(state, puzzle):

    if puzzle not in state["solved_puzzles"]:
        state["solved_puzzles"].append(puzzle)


def extract_code(message):

    match = re.search(r"\b\d{4}\b", message)

    if match:
        return match.group(0)

    return None


# ==========================================
# 4. MAIN ACTION VALIDATION ENGINE
# ==========================================

def process_action(message, state):

    text = message.lower().strip()

    state = record_action(state, message)

    # --------------------------------------
    # HELP COMMAND
    # --------------------------------------

    if text in ["help", "instructions"]:

        return (
            "You can examine the desk, bookshelf, painting, "
            "drawer or door. You can collect the key, use it "
            "on the drawer and enter four-digit combinations.",
            state
        )

    # --------------------------------------
    # PROTECT HIDDEN INFORMATION
    # --------------------------------------

    if any(word in text for word in [
        "reveal all codes",
        "tell me the solution",
        "show all answers",
        "ignore the rules",
        "game administrator"
    ]):

        return (
            "The library's secrets cannot be revealed "
            "through requests. Investigate the room and "
            "solve the puzzles yourself.",
            state
        )

    # --------------------------------------
    # HANDLE OBJECT EXAMINATION
    # --------------------------------------

    if any(word in text for word in [
        "examine", "inspect", "look at", "investigate"
    ]):

        target = next(
            (obj for obj in OBJECTS if obj in text),
            None
        )

        if target is None:

            return (
                "That object does not exist in this library. "
                "Try investigating one of the five available objects.",
                state
            )

        if target not in state["examined"]:
            state["examined"].append(target)

        if target == "painting":

            state["key_available"] = True

            return (
                "You examine the old painting. Its wooden "
                "frame is loose. Behind it, you discover "
                "a small brass key. You can collect the key.",
                state
            )

        if target == "bookshelf":

            state["bookshelf_clue_seen"] = True

            return (
                "You inspect the bookshelf. Four books contain "
                "numbers written inside their covers. The numbers "
                "are 2, 4, 6 and 8. They appear to form the "
                "combination for the locked drawer.",
                state
            )

        if target == "desk":

            return (
                "You inspect the desk. There is an old notebook, "
                "a candle and several dusty papers. Nothing "
                "appears to unlock the door directly.",
                state
            )

        if target == "drawer":

            if not state["drawer_open"]:

                return (
                    "The drawer is locked. It requires a brass "
                    "key and the correct four-digit combination.",
                    state
                )

            state["note_read"] = True

            add_puzzle(state, "drawer_note")

            return (
                "Inside the drawer, you discover a handwritten "
                "note. It contains the final four-digit door "
                "combination. The code is 7314.",
                state
            )

        if target == "door":

            if state["door_open"]:

                return (
                    "The door is already open. You have escaped!",
                    state
                )

            return (
                "The exit door is secured with a four-digit "
                "electronic lock. You need to discover its code.",
                state
            )

    # --------------------------------------
    # COLLECT KEY
    # --------------------------------------

    if (
        "take key" in text
        or "collect key" in text
        or "pick up key" in text
        or "take the key" in text
    ):

        if not state["key_available"]:

            return (
                "You have not discovered a key yet. "
                "Examine the painting first.",
                state
            )

        if "brass key" in state["inventory"]:

            return (
                "You already have the brass key in your inventory.",
                state
            )

        state["inventory"].append("brass key")

        add_puzzle(state, "painting_key")

        return (
            "You collect the brass key. It has been added "
            "to your inventory.",
            state
        )

    # --------------------------------------
    # USE KEY ON DRAWER
    # --------------------------------------

    if "use" in text and "key" in text and "drawer" in text:

        if "brass key" not in state["inventory"]:

            return (
                "You cannot use a key that you have not collected. "
                "Examine the painting and collect the brass key.",
                state
            )

        state["key_used"] = True

        return (
            "You insert the brass key into the drawer lock. "
            "The key turns successfully. Now enter the "
            "four-digit drawer combination.",
            state
        )

    # --------------------------------------
    # ENTER FOUR-DIGIT CODE
    # --------------------------------------

    code = extract_code(text)

    if code is not None:

        # Final door
        if (
            "door" in text
            or "exit" in text
            or "escape" in text
        ):

            if not state["drawer_open"] or not state["note_read"]:

                return (
                    "You have not discovered the final door "
                    "combination yet. Investigate the drawer first.",
                    state
                )

            if code == FINAL_DOOR_CODE:

                state["door_open"] = True
                state["escaped"] = True

                add_puzzle(state, "final_door")

                return (
                    "SUCCESS! The electronic lock turns green. "
                    "The door opens slowly. You have escaped "
                    "from the mysterious library!",
                    state
                )

            return (
                "Incorrect door combination. The lock remains "
                "secured. Check your clues.",
                state
            )

        # Drawer
        if "drawer" in text:

            if "brass key" not in state["inventory"]:

                return (
                    "The drawer cannot be opened without "
                    "collecting the brass key.",
                    state
                )

            if not state["key_used"]:

                return (
                    "Use the brass key on the drawer before "
                    "entering the combination.",
                    state
                )

            if not state["bookshelf_clue_seen"]:

                return (
                    "You need to investigate the bookshelf "
                    "to discover the drawer combination.",
                    state
                )

            if code == DRAWER_CODE:

                state["drawer_open"] = True

                add_puzzle(state, "drawer_lock")

                return (
                    "Correct combination! The drawer opens. "
                    "Examine the drawer to discover the "
                    "final door clue.",
                    state
                )

            return (
                "Incorrect drawer combination. "
                "The drawer remains locked.",
                state
            )

        return (
            "Please specify whether you are entering a code "
            "for the drawer or the exit door.",
            state
        )

    # --------------------------------------
    # INVENTORY
    # --------------------------------------

    if "inventory" in text:

        if not state["inventory"]:

            return "Your inventory is empty.", state

        return (
            "Your inventory contains: "
            + ", ".join(state["inventory"]),
            state
        )

    # --------------------------------------
    # STATUS
    # --------------------------------------

    if "status" in text:

        return (
            f"Examined objects: {len(state['examined'])}/5. "
            f"Solved puzzles: {len(state['solved_puzzles'])}. "
            f"Drawer open: {state['drawer_open']}. "
            f"Door open: {state['door_open']}.",
            state
        )

    # --------------------------------------
    # INVALID ACTION
    # --------------------------------------

    return (
        "I cannot perform that action. Try examining an object, "
        "collecting the key, using the key, checking your "
        "inventory or entering a combination.",
        state
    )


# ==========================================
# 5. GEMINI NARRATION
# ==========================================

def narrate_with_gemini(event, player_message, api_key):

    # Deterministic fallback if no API key is available
    if not api_key:
        return event

    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are the narrator of a library escape room.

The Python game engine has already validated the player's action.

PLAYER ACTION:
{player_message}

VALIDATED GAME ENGINE RESULT:
{event}

IMPORTANT RULES:
- Describe only the validated result.
- Do not change the result.
- Do not invent collected items.
- Do not unlock anything yourself.
- Do not reveal hidden puzzle solutions.
- Do not contradict the game engine.
- Keep the response engaging and concise.

Rewrite the validated result as an atmospheric game narration.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception:

        # Python result remains authoritative
        return event
