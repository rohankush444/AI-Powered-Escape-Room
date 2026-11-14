
from google import genai


GAME_RULES = """
You are the Game Master of a mysterious library escape room.

STORY:
The player wakes up inside a locked library.

OBJECTS:
1. Desk
2. Bookshelf
3. Painting
4. Locked drawer
5. Exit door

PUZZLE DESIGN:
- Examining the painting reveals a small brass key.
- The bookshelf contains a clue to the drawer combination.
- The drawer combination is 2468.
- The locked drawer contains a note with the final door code: 7314.
- The final door code is 7314.

INSTRUCTIONS:
- Respond naturally and make the game interesting.
- Describe objects when the player examines them.
- Remember previous messages.
- Do not invent new objects or change the puzzle solutions.
- Encourage the player to investigate.
- The player must find the key, solve the drawer puzzle,
  and discover the final door code.
- If the player enters 7314 for the exit door, describe
  the door opening and the player escaping.
- Never reveal all puzzle answers immediately.
- Keep responses clear and reasonably short.
"""


def get_gemini_response(message, history, api_key):

    if not api_key:
        return (
            "The library is quiet and mysterious. "
            "You can investigate the desk, bookshelf, "
            "painting, locked drawer or exit door. "
            "Try examining the bookshelf first."
        )

    try:
        client = genai.Client(api_key=api_key)

        conversation = ""

        for item in history[-12:]:
            role = item.get("role", "user")
            content = item.get("content", "")
            conversation += f"\n{role}: {content}"

        prompt = f"""
{GAME_RULES}

PREVIOUS CONVERSATION:
{conversation}

CURRENT PLAYER MESSAGE:
{message}

Respond as the Game Master.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return (
            "The Game Master encountered an API problem. "
            f"Please try again. Technical details: {str(e)[:250]}"
        )


def chat_v1(message, history, api_key):

    return get_gemini_response(
        message,
        history or [],
        api_key
    )
