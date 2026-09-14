import unittest
from src.capacity import estimate, join_cardinality


class CapacityTest(unittest.TestCase):
    def test_resource_and_runtime_arithmetic(self):
        self.assertEqual(estimate(hours=2)["dpu_hours"], 120)
        self.assertEqual(estimate(hours=3)["dpu_hours"], 180)
        self.assertEqual(estimate()["nominal_vcpu"], 240)
        self.assertEqual(estimate()["nominal_memory_gb"], 960)
        self.assertAlmostEqual(estimate()["equivalent_input_rows_per_second"], 69444.4444, places=3)

    def test_cardinality_explosion_is_separate_from_skew(self):
        self.assertEqual(join_cardinality({"hot": 500_000_000}, {"hot": 2000}), 1_000_000_000_000)
        self.assertEqual(join_cardinality({"hot": 500_000_000}, {"hot": 1}), 500_000_000)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            estimate(hours=0)
