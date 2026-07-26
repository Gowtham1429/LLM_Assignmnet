"""
Centralized configuration, loaded entirely from environment variables.
No secrets or magic numbers are hardcoded elsewhere in the codebase.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    return int(os.environ.get(name, default))


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", "")
    generation_model: str = os.environ.get("GENERATION_MODEL", "claude-sonnet-4-5")
    embedding_model: str = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    chunk_size: int = _int("CHUNK_SIZE", 800)
    chunk_overlap: int = _int("CHUNK_OVERLAP", 120)

    top_k: int = _int("TOP_K", 5)

    chroma_persist_dir: str = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_store")
    chroma_collection: str = os.environ.get("CHROMA_COLLECTION", "rag_corpus")

    api_host: str = os.environ.get("API_HOST", "0.0.0.0")
    api_port: int = _int("API_PORT", 8000)

    log_file: str = os.environ.get("LOG_FILE", "./results/query_log.jsonl")


settings = Settings()
