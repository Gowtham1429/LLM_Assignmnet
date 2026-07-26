import math

EMBEDDING_DIMENSION = 384
BYTES_PER_NUMBER = 4
METADATA_BYTES = 200
SELF_HOSTED_VM_COST = 45.0
STORAGE_COST_PER_GB = 0.10
MANAGED_POD_COST = 70.0
VECTORS_PER_POD = 1000000


def vector_storage_gb(num_vectors):
    bytes_per_vector = EMBEDDING_DIMENSION * BYTES_PER_NUMBER + METADATA_BYTES
    total_bytes = num_vectors * bytes_per_vector
    return total_bytes / (1024 * 1024 * 1024)


def self_hosted_cost(num_vectors):
    storage = vector_storage_gb(num_vectors)
    return SELF_HOSTED_VM_COST + storage * STORAGE_COST_PER_GB


def managed_cost(num_vectors):
    pods = math.ceil(num_vectors / VECTORS_PER_POD)
    if pods < 1:
        pods = 1
    return pods * MANAGED_POD_COST


def build_cost_table():
    scales = [100000, 1000000, 10000000]
    rows = []

    for scale in scales:
        self_cost = self_hosted_cost(scale)
        managed = managed_cost(scale)
        savings = ((managed - self_cost) / managed) * 100

        rows.append({
            "vectors": scale,
            "self_hosted_monthly": round(self_cost, 2),
            "managed_monthly": round(managed, 2),
            "savings_percent": round(savings, 1)
        })

    return rows


if __name__ == "__main__":
    for row in build_cost_table():
        print(row)
