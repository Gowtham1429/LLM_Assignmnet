from src.compare import compare_answers

def check_position_bias(question, expected_answer, answer_a, answer_b):
    normal = compare_answers(question, expected_answer, answer_a, answer_b)
    swapped = compare_answers(question, expected_answer, answer_b, answer_a)

    normal_winner = normal.get("winner")
    swapped_winner = swapped.get("winner")

    if swapped_winner == "A":
        mapped_winner = "B"
    elif swapped_winner == "B":
        mapped_winner = "A"
    else:
        mapped_winner = swapped_winner

    position_flip = normal_winner != mapped_winner

    return {
        "normal_winner": normal_winner,
        "swapped_mapped_winner": mapped_winner,
        "position_flip": position_flip
    }
