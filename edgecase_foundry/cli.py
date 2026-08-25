import argparse
import json

from .compiler import compile_hypothesis
from .generator import generate_sequences, scenario_record
from .replay import evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile and replay a model stress scenario")
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--count", type=int, default=200)
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()

    scenario = compile_hypothesis(args.hypothesis)
    sequences = generate_sequences(scenario, args.count, args.seed)
    report = {
        "scenario": scenario_record(scenario),
        "generated_sequences": len(sequences),
        "model_replay": evaluate(sequences),
        "claim_scope": "fixture stress-test result; not production fraud performance",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
