import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)


def generate_answer(question, chunks):
    if len(chunks) == 0:
        return "I don't have enough information to answer this.", 0, 0

    context = ""

    for i in range(len(chunks)):
        context = context + "[" + str(i + 1) + "] " + chunks[i] + "\n\n"

    prompt = """
Answer the question using only the given context.

If the answer is not available in the context, say:
\"I don't have enough information to answer this.\"

Mention the chunk number used for the answer like [1] or [2].

Context:
""" + context + """

Question:
""" + question

    response = client.messages.create(
        model=os.environ.get("GENERATION_MODEL", "claude-sonnet-4-5"),
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    return answer, input_tokens, output_tokens
