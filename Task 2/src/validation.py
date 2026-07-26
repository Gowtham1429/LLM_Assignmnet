def validate_against_gold(results):
    correct = 0
    total = 0

    for result in results:
        gold = result.get("gold_winner")
        predicted = result["comparison"].get("winner")

        if gold:
            total += 1

            if gold == predicted:
                correct += 1

    agreement = 0

    if total > 0:
        agreement = correct / total

    return {
        "validated_cases": total,
        "judge_gold_agreement": round(agreement, 3)
    }


def calculate_flip_rate(results):
    flips = 0

    for result in results:
        if result["bias"]["position_flip"]:
            flips += 1

    if len(results) == 0:
        return 0

    return round(flips / len(results), 3)
