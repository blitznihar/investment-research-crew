import json
import os
from typing import Dict, Any

STATE_FILE = os.getenv("STATE_FILE", "state.json")


def _load() -> Dict[str, Any]:
    """
    Docstring for _load

    :return: Description
    :rtype: Dict[str, Any]
    """
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(state: Dict[str, Any]) -> None:
    """
    Docstring for _save
    """
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def already_processed(run_id: str, message_id: str) -> bool:
    """
    Docstring for already_processed

    :param run_id: Description
    :type run_id: str
    :param message_id: Description
    :type message_id: str
    :return: Description
    :rtype: bool
    """
    state = _load()
    processed = state.get(run_id, {}).get("processed_message_ids", [])
    return message_id in processed


def mark_processed(run_id: str, message_id: str, step: str, output: str = "") -> None:
    """
    Docstring for mark_processed

    :param run_id: Description
    :type run_id: str
    :param message_id: Description
    :type message_id: str
    :param step: Description
    :type step: str
    :param output: Description
    :type output: str
    """
    state = _load()
    run = state.setdefault(run_id, {})
    processed = run.setdefault("processed_message_ids", [])
    if message_id not in processed:
        processed.append(message_id)

    outputs = run.setdefault("outputs", {})
    if output:
        outputs[step] = output

    run["last_step"] = step
    _save(state)


def get_state(run_id: str) -> Dict[str, Any]:
    """
    Docstring for get_state

    :param run_id: Description
    :type run_id: str
    :return: Description
    :rtype: Dict[str, Any]
    """
    return _load().get(run_id, {})
