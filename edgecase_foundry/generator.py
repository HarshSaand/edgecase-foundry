import random
from dataclasses import asdict

from .scenario import Scenario


HOME_CITIES = ["New York", "Boston", "Chicago", "Seattle"]


def generate_sequences(scenario: Scenario, count: int, seed: int) -> list[list[dict]]:
    rng = random.Random(seed)
    sequences = []
    for account_index in range(count):
        home_city = rng.choice(HOME_CITIES)
        minute = 0
        events = []
        for _ in range(scenario.small_count):
            minute += rng.randint(1, max(1, scenario.window_minutes // (scenario.small_count + 1)))
            events.append(
                {
                    "account_id": f"stress-{account_index:05d}",
                    "minute": minute,
                    "amount": round(rng.uniform(0.5, scenario.small_max_amount), 2),
                    "channel": "chip",
                    "city": home_city,
                    "label": 0,
                }
            )
        final_city = rng.choice([city for city in HOME_CITIES if city != home_city]) if scenario.require_new_city else home_city
        minute = min(scenario.window_minutes, minute + 1)
        events.append(
            {
                "account_id": f"stress-{account_index:05d}",
                "minute": minute,
                "amount": round(rng.uniform(scenario.final_min_amount, scenario.final_min_amount * 1.8), 2),
                "channel": scenario.final_channel,
                "city": final_city,
                "label": 1,
            }
        )
        sequences.append(events)
    return sequences


def scenario_record(scenario: Scenario) -> dict:
    return asdict(scenario)
