import argparse
import json
import time
from pyspark.sql import SparkSession, functions as F
from src.lab import generate, assert_unique_dimension, configure, join


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=50_000)
    parser.add_argument("--mode", choices=["baseline", "aqe", "salt", "broadcast"],
                        default="baseline")
    args = parser.parse_args()
    spark = (SparkSession.builder.master("local[2]").appName("spark-skew-lab")
             .config("spark.sql.shuffle.partitions", "8").getOrCreate())
    try:
        configure(spark, args.mode)
        facts, dimension = generate(spark, rows=args.rows)
        assert_unique_dimension(dimension)
        joined = join(facts, dimension, mode=args.mode)
        started = time.perf_counter()
        # Agregação dependente de ambos os lados para materializar o join.
        query = joined.agg(F.count("*").alias("rows"),
                           F.sum("score").alias("score_sum"),
                           F.sum(F.length("owner")).alias("owner_length_sum"))
        result = query.first().asDict()
        elapsed = time.perf_counter() - started
        print(json.dumps({"mode": args.mode, "spark_version": spark.version,
                          "elapsed_seconds": elapsed, "result": result,
                          "synthetic": True, "scope": "join+aggregate, local[2]"},
                         sort_keys=True))
        query.explain(mode="formatted")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
