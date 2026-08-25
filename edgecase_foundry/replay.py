def baseline_predict(event: dict) -> int:
    """Transparent placeholder model used to make stress failures inspectable."""
    is_large = event["amount"] >= 1000
    risky_channel = event["channel"] == "online"
    return int(is_large and risky_channel)


def evaluate(sequences: list[list[dict]]) -> dict[str, float]:
    positives = 0
    detected = 0
    for sequence in sequences:
        for event in sequence:
            if event["label"] == 1:
                positives += 1
                detected += baseline_predict(event)
    recall = detected / positives if positives else 0.0
    return {"positive_events": positives, "detected": detected, "recall": recall}
