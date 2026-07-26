import sys
import time

from src.retrieve import retrieve
from src.generate import generate_answer
from src.logger import log_query


def main():
    if len(sys.argv) < 2:
        print("Please enter a question")
        return

    question = sys.argv[1]
    start_time = time.time()

    chunks = retrieve(question, 3)
    answer, input_tokens, output_tokens = generate_answer(question, chunks)

    end_time = time.time()
    latency = (end_time - start_time) * 1000

    log_query(
        question,
        latency,
        len(chunks),
        input_tokens,
        output_tokens
    )

    print("Answer:", answer)
    print("Chunks used:", len(chunks))
    print("Input tokens:", input_tokens)
    print("Output tokens:", output_tokens)
    print("Latency:", round(latency, 2), "ms")


if __name__ == "__main__":
    main()
