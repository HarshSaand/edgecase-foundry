import re

from .scenario import Scenario


NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def _small_count(text: str) -> int:
    for word, number in NUMBER_WORDS.items():
        if re.search(rf"\b{word}\b", text):
            return number
    match = re.search(r"(\d+)\s+small", text)
    return int(match.group(1)) if match else 3


def compile_hypothesis(text: str) -> Scenario:
    """Small auditable baseline; an LLM compiler will implement the same contract."""
    lowered = text.lower()
    amount = re.search(r"(?:above|over)\s*\$?(\d+(?:\.\d+)?)", lowered)
    window = re.search(r"within\s+(\d+)\s+minutes?", lowered)
    if not amount or not window:
        raise ValueError("hypothesis needs a final amount and time window")

    scenario = Scenario(
        small_count=_small_count(lowered),
        small_max_amount=5.0,
        final_min_amount=float(amount.group(1)),
        window_minutes=int(window.group(1)),
        final_channel="online" if "online" in lowered else "chip",
        require_new_city="new city" in lowered or "another city" in lowered,
    )
    scenario.validate()
    return scenario
