import json

from src.judge import judge_answer
from src.compare import compare_answers
from src.bias_check import check_position_bias
from src.report import save_report

def main():
    file = open("data/test_cases.json", "r", encoding="utf-8")
    tests = json.load(file)
    file.close()

    results = []

    for test in tests:
        print("Evaluating case:", test["id"])

        score_a = judge_answer(
            test["question"],
            test["expected_answer"],
            test["answer_a"]
        )

        score_b = judge_answer(
            test["question"],
            test["expected_answer"],
            test["answer_b"]
        )

        comparison = compare_answers(
            test["question"],
            test["expected_answer"],
            test["answer_a"],
            test["answer_b"]
        )

        bias = check_position_bias(
            test["question"],
            test["expected_answer"],
            test["answer_a"],
            test["answer_b"]
        )

        results.append({
            "id": test["id"],
            "gold_winner": test["gold_winner"],
            "score_a": score_a,
            "score_b": score_b,
            "comparison": comparison,
            "bias": bias
        })

    report = save_report(results)

    print("Evaluation completed")
    print("Total cases:", report["total_cases"])
    print("Position flip rate:", report["position_flip_rate"])
    print("Judge/gold agreement:", report["validation"]["judge_gold_agreement"])

if __name__ == "__main__":
    main()
