import json
import os
import re
import string
import anthropic


def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def exact_match(prediction, gold):
    if normalize_text(prediction) == normalize_text(gold):
        return 1
    return 0


def f1_score(prediction, gold):
    prediction_words = normalize_text(prediction).split()
    gold_words = normalize_text(gold).split()

    if len(prediction_words) == 0 or len(gold_words) == 0:
        return 0

    common = 0
    used = []

    for word in prediction_words:
        for i in range(len(gold_words)):
            if word == gold_words[i] and i not in used:
                common += 1
                used.append(i)
                break

    if common == 0:
        return 0

    precision = common / len(prediction_words)
    recall = common / len(gold_words)
    return 2 * precision * recall / (precision + recall)


def judge_answer(question, context, answer):
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        return {"faithfulness": None, "relevance": None}

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
Evaluate this RAG answer.
Give faithfulness and relevance scores from 1 to 5.
Return only JSON like:
{{"faithfulness": 5, "relevance": 5}}

Question:
{question}

Context:
{context}

Answer:
{answer}
"""

    response = client.messages.create(
        model=os.environ.get("GENERATION_MODEL", "claude-sonnet-4-5"),
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text

    try:
        return json.loads(text)
    except:
        return {"faithfulness": None, "relevance": None}
