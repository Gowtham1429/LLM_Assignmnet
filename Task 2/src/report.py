import json
import os

from src.validation import validate_against_gold, calculate_flip_rate

def save_report(results):
    os.makedirs("results", exist_ok=True)

    a_wins = 0
    b_wins = 0
    ties = 0

    for result in results:
        winner = result["comparison"].get("winner")

        if winner == "A":
            a_wins += 1
        elif winner == "B":
            b_wins += 1
        elif winner == "TIE":
            ties += 1

    validation = validate_against_gold(results)

    report = {
        "total_cases": len(results),
        "answer_a_wins": a_wins,
        "answer_b_wins": b_wins,
        "ties": ties,
        "position_flip_rate": calculate_flip_rate(results),
        "validation": validation,
        "results": results
    }

    file = open("results/report.json", "w", encoding="utf-8")
    json.dump(report, file, indent=2)
    file.close()

    return report
