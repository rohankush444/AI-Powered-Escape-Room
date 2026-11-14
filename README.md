# AI-Powered Escape Room

An interactive escape room application developed using Python, Google Gemini API and Gradio.

## 1. Project Overview

The player wakes up inside a locked library. They must investigate objects, discover clues, solve puzzles and unlock the exit door.

The project demonstrates two approaches to building an AI-powered game: an LLM-driven approach in Version 1 and a structured, rule-based approach in Version 2.

## 2. Technologies

- Python
- Google Gemini API
- Gradio
- Pytest
- Git and GitHub

## 3. Version 1 - AI Game Master

Version 1 uses Gemini as the Game Master.

Features:
- Natural-language interaction
- Conversation history
- AI-generated game responses
- Interactive library objects

Limitation: The language model may misunderstand actions or produce inconsistent game progress.

## 4. Version 2 - Structured Game Logic

Version 2 introduces deterministic Python-based game management.

Features:
- Structured game state
- Inventory tracking
- Action validation
- Puzzle and code validation
- Invalid-action handling
- Consistent game progression

Python determines whether an action is valid before the game state is updated.

## 5. Interactive Objects

1. Desk
2. Bookshelf
3. Painting
4. Locked drawer
5. Exit door

## 6. Puzzle Sequence

The player investigates the library, collects a brass key, discovers the drawer combination, opens the drawer and finds the final door code.

- Drawer code: 2468
- Exit door code: 7314

## 7. Installation

Clone the repository:

    git clone https://github.com/rohankush444/AI-Powered-Escape-Room.git

Enter the project directory:

    cd AI-Powered-Escape-Room

Install dependencies:

    pip install -r requirements.txt

## 8. API Configuration

Set the environment variable GEMINI_API_KEY to your Gemini API key.

For Google Colab, add the key through Colab Secrets.

Never upload your real API key to GitHub.

## 9. Run the Application

    python app.py

Open the Gradio link displayed when the application starts.

## 10. Run Tests

    pytest -v tests/

See test_cases.md for additional test scenarios.

## 11. Architecture

- architecture_v1.mmd
- architecture_v2.mmd

## 12. Project Report

See report.md for implementation details, challenges, testing and improvements.

## 13. Screenshots and Demonstration

Screenshots of the actual running application should be added to the screenshots/ directory.

Add a link to the demonstration video after recording it.

## 14. Limitations and Future Improvements

- The application currently uses one library room.
- AI responses depend on Gemini API availability and model access.
- Additional rooms, puzzles, scoring and richer visual interactions could be added in future versions.

## 15. Author

Rohan Ramashray Kushwaha

University of Europe for Applied Sciences

M.Sc. Data Science
