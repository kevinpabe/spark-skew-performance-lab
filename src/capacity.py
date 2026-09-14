"""Aritmética de capacidade; não é um preditor de runtime."""
import json


def estimate(rows=500_000_000, workers=30, hours=2.0, bytes_per_row=200):
    if any(v <= 0 for v in (rows, workers, hours, bytes_per_row)):
        raise ValueError("Entradas devem ser positivas")
    dpus = workers * 2
    return {
        "rows": rows, "workers_g2x": workers, "hours": hours,
        "dpu": dpus, "nominal_vcpu": workers * 8,
        "nominal_memory_gb": workers * 32,
        "dpu_hours": dpus * hours,
        "equivalent_input_rows_per_second": rows / (hours * 3600),
        "logical_input_gb": rows * bytes_per_row / 1_000_000_000,
        "assumed_bytes_per_row": bytes_per_row,
        "runtime_validated": False,
    }


def join_cardinality(left_counts, right_counts):
    """Cardinalidade de inner equijoin para contagens por chave não nula."""
    if any(v < 0 for v in list(left_counts.values()) + list(right_counts.values())):
        raise ValueError("Contagem negativa")
    return sum(n * right_counts.get(k, 0) for k, n in left_counts.items() if k is not None)


if __name__ == "__main__":
    print(json.dumps([estimate(hours=h) for h in (2, 3)], indent=2))
