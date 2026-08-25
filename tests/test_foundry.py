import unittest

from edgecase_foundry.compiler import compile_hypothesis
from edgecase_foundry.generator import generate_sequences


HYPOTHESIS = "three small purchases then an online purchase above 700 within 20 minutes from a new city"


class FoundryTest(unittest.TestCase):
    def test_compiler_produces_expected_contract(self):
        scenario = compile_hypothesis(HYPOTHESIS)
        self.assertEqual(scenario.small_count, 3)
        self.assertEqual(scenario.final_min_amount, 700)
        self.assertTrue(scenario.require_new_city)

    def test_generated_sequence_satisfies_constraints(self):
        scenario = compile_hypothesis(HYPOTHESIS)
        sequence = generate_sequences(scenario, count=1, seed=9)[0]
        self.assertEqual(len(sequence), 4)
        self.assertTrue(all(event["amount"] <= 5 for event in sequence[:-1]))
        self.assertGreaterEqual(sequence[-1]["amount"], 700)
        self.assertLessEqual(sequence[-1]["minute"], 20)
        self.assertNotEqual(sequence[0]["city"], sequence[-1]["city"])

    def test_generation_is_reproducible(self):
        scenario = compile_hypothesis(HYPOTHESIS)
        self.assertEqual(generate_sequences(scenario, 3, 22), generate_sequences(scenario, 3, 22))


if __name__ == "__main__":
    unittest.main()
