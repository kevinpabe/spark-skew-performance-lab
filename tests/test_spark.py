import unittest
from pyspark.sql import SparkSession, functions as F
from src.lab import generate, assert_unique_dimension, configure, join


class SparkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = (SparkSession.builder.master("local[2]").appName("skew-tests")
                     .config("spark.ui.enabled", "false")
                     .config("spark.sql.shuffle.partitions", "4").getOrCreate())
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_strategies_preserve_full_multiset(self):
        facts, dimension = generate(self.spark, rows=400, assets=8)
        assert_unique_dimension(dimension)
        configure(self.spark, "baseline")
        baseline = join(facts, dimension)
        rows = baseline.collect()  # Apenas 400 linhas; não usar collect em produção.
        self.assertEqual(len(rows), 400)
        for mode in ("aqe", "salt", "broadcast"):
            configure(self.spark, mode)
            candidate = join(facts, dimension, mode=mode)
            # Compara o multiconjunto completo da fixture, incluindo duplicidades.
            self.assertCountEqual(rows, candidate.collect(), mode)

    def test_duplicate_dimension_is_rejected_before_join(self):
        _, dimension = generate(self.spark, rows=20, assets=4)
        duplicated = dimension.unionByName(dimension.filter(F.col("asset_id") == 0))
        with self.assertRaisesRegex(ValueError, "many-to-one"):
            assert_unique_dimension(duplicated)

    def test_selective_salt_only_expands_hot_dimension(self):
        facts, dimension = generate(self.spark, rows=40, assets=4)
        self.assertEqual(join(facts, dimension, "salt", salt_buckets=3).count(), 40)

    def test_unknown_mode_is_rejected(self):
        facts, dimension = generate(self.spark, rows=10)
        with self.assertRaises(ValueError):
            join(facts, dimension, "unknown")
