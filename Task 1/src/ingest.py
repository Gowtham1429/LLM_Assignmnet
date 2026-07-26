import os
import sys

from src.parsers import extract_text
from src.chunking import chunk_text
from src.embed import embed_texts
from src.store import store_chunks


def ingest_file(path, chunk_size=800, chunk_overlap=120):
    text = extract_text(path)
    chunks = chunk_text(text, chunk_size, chunk_overlap)

    if len(chunks) == 0:
        return {"file": path, "new": 0, "existing": 0}

    texts = []
    for chunk in chunks:
        texts.append(chunk.text)

    embeddings = embed_texts(texts)
    filename = os.path.basename(path)
    doc_type = filename.split(".")[-1].lower()

    new_count, existing_count = store_chunks(
        filename,
        doc_type,
        texts,
        embeddings
    )

    return {
        "file": filename,
        "new": new_count,
        "existing": existing_count
    }


def ingest_directory(folder):
    results = []

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        lower_name = filename.lower()

        if lower_name.endswith((".md", ".html", ".htm", ".pdf")):
            results.append(ingest_file(path))

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter a file or folder path")
    elif os.path.isdir(sys.argv[1]):
        print(ingest_directory(sys.argv[1]))
    else:
        print(ingest_file(sys.argv[1]))
