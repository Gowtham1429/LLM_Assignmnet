import os
import anthropic

from src.config import JUDGE_MODEL, MAX_TOKENS
from src.logger import log_judge
from src.utils import parse_json

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def compare_answers(question, expected_answer, answer_a, answer_b):
    prompt = """
You are an independent judge comparing two answers.

Use the expected answer as the main reference.
Do not prefer an answer because it is first, longer, more confident, or more stylish.
Choose A, B, or TIE.
Give a short reason.
Return only valid JSON.

Question:
""" + question + """

Expected answer:
""" + expected_answer + """

Answer A:
""" + answer_a + """

Answer B:
""" + answer_b + """

Return:
{
  "winner": "A",
  "reason": ""
}
"""

    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text
    result = parse_json(raw)

    if result is None:
        result = {"winner": "ERROR", "reason": "Invalid JSON"}

    log_judge({
        "type": "comparison",
        "model": JUDGE_MODEL,
        "question": question,
        "prompt": prompt,
        "raw_response": raw,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    })

    return result
