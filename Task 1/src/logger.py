import json
import os


def log_query(question, latency, num_chunks, input_tokens, output_tokens):
    record = {
        "question": question,
        "latency_ms": round(latency, 2),
        "num_chunks": num_chunks,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

    os.makedirs("results", exist_ok=True)
    log_file = open("results/query_log.jsonl", "a", encoding="utf-8")
    log_file.write(json.dumps(record) + "\n")
    log_file.close()
