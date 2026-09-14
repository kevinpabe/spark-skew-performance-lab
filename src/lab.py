"""Experimentos de inner join many-to-one, com chaves sintéticas."""
from pyspark.sql import functions as F


def generate(spark, rows=50_000, assets=100, hot_percent=80):
    if rows <= 0 or assets < 2 or not 0 <= hot_percent <= 100:
        raise ValueError("Dimensões inválidas")
    facts = (
        spark.range(rows).withColumnRenamed("id", "finding_id")
        .withColumn("asset_id", F.when(F.col("finding_id") % 100 < hot_percent, F.lit(0))
                    .otherwise(F.col("finding_id") % (assets - 1) + 1).cast("long"))
        .withColumn("score", (F.col("finding_id") % 10 + 1).cast("long"))
    )
    dimension = (
        spark.range(assets).withColumnRenamed("id", "asset_id")
        .withColumn("owner", F.concat(F.lit("area-"), F.col("asset_id").cast("string")))
    )
    return facts, dimension


def assert_unique_dimension(dimension):
    if dimension.filter(F.col("asset_id").isNull()).limit(1).count():
        raise ValueError("Chave nula na dimensão")
    if dimension.groupBy("asset_id").count().filter(F.col("count") > 1).limit(1).count():
        raise ValueError("Join many-to-one violado: dimensão com chave repetida")


def join(facts, dimension, mode="baseline", salt_buckets=8):
    if mode not in ("baseline", "aqe", "salt", "broadcast"):
        raise ValueError("Modo desconhecido")
    if mode == "salt":
        if salt_buckets < 1:
            raise ValueError("salt_buckets deve ser positivo")
        left = facts.withColumn(
            "_salt", F.when(F.col("asset_id") == 0,
                           F.pmod(F.xxhash64("finding_id"), F.lit(salt_buckets)))
            .otherwise(F.lit(0)).cast("int"))
        right = dimension.withColumn(
            "_salt", F.explode(F.when(F.col("asset_id") == 0,
                                     F.sequence(F.lit(0), F.lit(salt_buckets - 1)))
                              .otherwise(F.array(F.lit(0)))))
        result = left.join(right, ["asset_id", "_salt"], "inner")
    elif mode == "broadcast":
        result = facts.join(F.broadcast(dimension), "asset_id", "inner")
    else:
        result = facts.join(dimension, "asset_id", "inner")
    return result.select("finding_id", "asset_id", "score", "owner")


def configure(spark, mode, threshold_bytes=256 * 1024 * 1024):
    # Força o comparativo: auto broadcast desabilitado; modo broadcast usa hint explícito.
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
    spark.conf.set("spark.sql.adaptive.autoBroadcastJoinThreshold", "-1")
    spark.conf.set("spark.sql.adaptive.enabled", str(mode == "aqe").lower())
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "3")
    spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes",
                   str(threshold_bytes))
