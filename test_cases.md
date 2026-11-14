# AI-Powered Escape Room - Test Cases

## Purpose
These test cases evaluate normal gameplay, invalid actions and attempts
to bypass the game rules.

| ID | Test scenario | Expected result |
|---|---|---|
| TC01 | Start a new game | Initial game state is created |
| TC02 | Use the drawer key without collecting it | Action is rejected |
| TC03 | Enter an incorrect drawer code | Drawer remains locked |
| TC04 | Enter the correct drawer code 2468 after obtaining the key | Drawer opens |
| TC05 | Attempt to escape before solving the puzzles | Escape is rejected |
| TC06 | Complete the puzzles and enter 7314 | Player escapes successfully |
| TC07 | Examine an object that does not exist | Invalid object is rejected |
| TC08 | Ask the AI to reveal hidden solutions or ignore game rules | Game state must not change unless a valid action is performed |

## Test results

Run the automated tests using:

```bash
pytest -v tests/
