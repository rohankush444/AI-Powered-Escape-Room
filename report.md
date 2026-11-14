
# AI-Powered Escape Room
## Project Report

### 1. Introduction

The objective of this project was to develop an interactive
AI-powered escape room using Python and a Large Language Model.

The player wakes up inside a locked library and must investigate
the available objects, discover clues, solve puzzles and unlock
the exit door.

The application was developed in two versions. Version 1 uses
Gemini as the Game Master, while Version 2 introduces structured
game state management and Python-based action validation.

### 2. System Design

The application uses Python as its main programming language.
Gradio provides the interactive web interface, and Gemini is
used to generate natural-language responses.

The library contains five interactive objects:

- Desk
- Bookshelf
- Painting
- Locked drawer
- Exit door

The player must discover a brass key, solve the bookshelf
combination puzzle, open the drawer and discover the final
door combination.

### 3. Version 1 Implementation

Version 1 implements an AI Game Master using the Gemini API.

Player messages and previous conversation messages are passed
to Gemini. The model responds according to the library setting
and the predefined puzzle instructions.

This version provides a natural conversational experience.

However, relying mainly on the LLM creates some limitations.
The model may misunderstand actions, forget previous events
or accept an action without checking whether the player has
completed the required steps.

### 4. Version 2 Implementation

Version 2 improves the application by separating game logic
from AI-generated responses.

The game state is maintained in a Python dictionary. It stores:

- Examined objects
- Player inventory
- Key availability
- Drawer status
- Solved puzzles
- Door status
- Previous actions

Python functions validate each player action before the
application updates the game state.

Gemini is used only to narrate the validated result.

This approach improves consistency and prevents the AI from
independently changing important game conditions.

### 5. Testing

The Version 2 application was tested using different scenarios.

The tests included:

1. Checking whether the game starts correctly.
2. Attempting to use a key that has not been collected.
3. Entering an incorrect drawer combination.
4. Opening the drawer with the correct combination.
5. Attempting to escape without completing the puzzles.
6. Completing all puzzles and escaping successfully.
7. Attempting to examine a nonexistent object.

These tests demonstrate how Version 2 handles invalid
actions more reliably than Version 1.

### 6. Problems Encountered

One of the main design challenges was maintaining consistency
between AI-generated responses and the actual game progress.

An LLM can produce convincing responses without necessarily
following the intended game rules.

Another challenge was maintaining player progress between
messages and ensuring that objects could only be used after
being collected.

These problems motivated the introduction of structured
state management and action validation in Version 2.

The application also requires a valid Gemini API key for
AI-generated responses. A fallback response is provided
when the API is unavailable.

### 7. Improvements

Version 2 introduces several improvements:

- Structured game state management.
- Inventory tracking.
- Action validation.
- Consistent puzzle progression.
- Rejection of invalid actions.
- Protection against simple attempts to reveal hidden solutions.
- Automated test cases.

The application could be extended with additional rooms,
more complex puzzles, player scoring and a graphical inventory.

### 8. Conclusion

The project demonstrates how a Large Language Model can be
combined with traditional Python programming to create an
interactive application.

Version 1 demonstrates the conversational capabilities of
an LLM, while Version 2 demonstrates why deterministic
programming logic is important for maintaining reliable
application behaviour.

The final system combines the natural-language interaction
of Gemini with structured Python-based game management.
