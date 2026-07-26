import os

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-sonnet-4-5")
MAX_TOKENS = int(os.environ.get("JUDGE_MAX_TOKENS", "900"))
