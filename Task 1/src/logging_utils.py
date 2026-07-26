"""
Per-query structured logging (JSON Lines): latency, chunk count, and
token usage for every /query call, appended to settings.log_file.
"""
import json
import time
from pathlib import Path


def log_query(
    question: str,
    latency_ms: float,
    num_chunks: int,
    input_tokens: int,
    output_tokens: int,
    log_file: str,
) -> None:
    record = {
        "timestamp": time.time(),
        "question": question,
        "latency_ms": round(latency_ms, 2),
        "num_chunks": num_chunks,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
