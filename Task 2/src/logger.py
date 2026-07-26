import json
import os
from datetime import datetime

def log_judge(record):
    os.makedirs("logs", exist_ok=True)
    record["time"] = datetime.now().isoformat()

    file = open("logs/judge_log.jsonl", "a", encoding="utf-8")
    file.write(json.dumps(record) + "\n")
    file.close()
