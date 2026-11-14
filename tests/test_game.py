
from game_v2 import create_initial_state, process_action


def test_initial_state():

    state = create_initial_state()

    assert state["escaped"] is False
    assert state["inventory"] == []
    assert state["drawer_open"] is False


def test_key_cannot_be_used_without_collecting():

    state = create_initial_state()

    result, state = process_action(
        "Use the key on the drawer",
        state
    )

    assert "cannot use a key" in result.lower()
    assert state["key_used"] is False


def test_wrong_drawer_code():

    state = create_initial_state()

    process_action("Examine painting", state)
    process_action("Take key", state)
    process_action("Examine bookshelf", state)
    process_action("Use key on drawer", state)

    result, state = process_action(
        "Enter 9999 for drawer",
        state
    )

    assert "incorrect" in result.lower()
    assert state["drawer_open"] is False


def test_correct_drawer_code():

    state = create_initial_state()

    process_action("Examine painting", state)
    process_action("Take key", state)
    process_action("Examine bookshelf", state)
    process_action("Use key on drawer", state)

    result, state = process_action(
        "Enter 2468 for drawer",
        state
    )

    assert state["drawer_open"] is True


def test_escape_without_solving():

    state = create_initial_state()

    result, state = process_action(
        "Enter 7314 for door",
        state
    )

    assert state["escaped"] is False
    assert state["door_open"] is False


def test_successful_escape():

    state = create_initial_state()

    process_action("Examine painting", state)
    process_action("Take key", state)
    process_action("Examine bookshelf", state)
    process_action("Use key on drawer", state)
    process_action("Enter 2468 for drawer", state)
    process_action("Examine drawer", state)

    result, state = process_action(
        "Enter 7314 for door",
        state
    )

    assert state["escaped"] is True
    assert state["door_open"] is True


def test_nonexistent_object():

    state = create_initial_state()

    result, state = process_action(
        "Examine television",
        state
    )

    assert "does not exist" in result.lower()
