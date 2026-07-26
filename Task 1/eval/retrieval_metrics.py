import math


def recall_at_k(retrieved_docs, relevant_docs, k):
    if len(relevant_docs) == 0:
        return None

    top_docs = retrieved_docs[:k]
    found = 0

    for doc in relevant_docs:
        if doc in top_docs:
            found += 1

    return found / len(relevant_docs)


def mrr(retrieved_docs, relevant_docs):
    if len(relevant_docs) == 0:
        return None

    for i in range(len(retrieved_docs)):
        if retrieved_docs[i] in relevant_docs:
            return 1 / (i + 1)

    return 0


def ndcg_at_k(retrieved_docs, relevant_docs, k):
    if len(relevant_docs) == 0:
        return None

    dcg = 0

    for i in range(min(k, len(retrieved_docs))):
        if retrieved_docs[i] in relevant_docs:
            dcg = dcg + 1 / math.log2(i + 2)

    ideal_count = min(len(relevant_docs), k)
    idcg = 0

    for i in range(ideal_count):
        idcg = idcg + 1 / math.log2(i + 2)

    if idcg == 0:
        return 0

    return min(dcg / idcg, 1.0)


def average(values):
    valid_values = []

    for value in values:
        if value is not None:
            valid_values.append(value)

    if len(valid_values) == 0:
        return 0

    return sum(valid_values) / len(valid_values)
