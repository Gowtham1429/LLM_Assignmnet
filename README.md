# Simple RAG Application

This project is a small Retrieval-Augmented Generation (RAG) application. It reads PDF, HTML, and Markdown files, splits the text into chunks, creates embeddings, stores them in ChromaDB, retrieves relevant chunks, and sends only those chunks to an LLM for answering.

## Main flow

1. `parsers.py` extracts plain text from PDF, HTML, and Markdown.
2. `chunking.py` divides the text into smaller overlapping chunks.
3. `embed.py` converts chunks into vectors using `all-MiniLM-L6-v2`.
4. `store.py` stores vectors and metadata in ChromaDB.
5. `retrieve.py` finds the most similar chunks for a question.
6. `generate.py` asks Claude to answer only from the retrieved context.
7. `query_cli.py` runs the full query flow and logs latency, chunk count, and token usage.

## Why ChromaDB?

I selected ChromaDB because it is simple to run locally, does not need a separate database server, supports metadata, and supports vector similarity search. For this student project it is easier and cheaper to operate than a managed vector database. A managed service would become more useful when the system needs high availability, automatic scaling, multi-region deployment, or very high query traffic.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

On Windows PowerShell:

```powershell
$env:ANTHROPIC_API_KEY="your_key_here"
```

## Ingest documents

The `sample_docs` folder contains Markdown, HTML, and PDF examples.

```bash
python -m src.ingest sample_docs
```

The chunk ID is created from the source document, chunk index, and chunk text using SHA-256. Before inserting, the program checks whether the ID already exists. This makes re-ingestion idempotent and avoids duplicate vectors.

Each chunk stores these metadata fields: `source_doc`, `doc_type`, and `chunk_index`. `search_chunks()` also supports filtering by `doc_type`.

## Ask a question

```bash
python -m src.query_cli "What are the storage tiers?"
```

Each query is appended to `results/query_log.jsonl`. The log includes question, latency, number of retrieved chunks, input tokens, and output tokens.

An optional FastAPI endpoint is also available:

```bash
uvicorn src.api:app --port 8000
```

## Evaluation

The fixed evaluation set is stored in `eval/qa_dataset.json`. It contains 28 questions with gold answers and relevant source-document labels.

Run:

```bash
python -m eval.run_eval
```

The evaluation calculates Recall@k, MRR, nDCG@k, Exact Match, F1, latency, and optional LLM-judge faithfulness/relevance scores. Results are saved to `results/eval_results.json`.

## Cost assumptions

The cost model is in `eval/cost_model.py`. These are illustrative assumptions, not live vendor prices:

| Vectors | Self-hosted Chroma / month | Managed DB / month |
|---:|---:|---:|
| 100,000 | $45.02 | $70.00 |
| 1,000,000 | $45.16 | $70.00 |
| 10,000,000 | $46.62 | $700.00 |

Assumptions: 384-dimensional float32 embeddings, about 200 bytes of metadata per vector, a $45/month self-hosted VM, $0.10/GB storage, and a managed pod costing $70/month with capacity for about 1 million vectors.

## Retrieval vs generation

For a small and clearly separated document set, retrieval should usually be the easier part because the embedding model only needs to find the correct document chunks. Generation is a larger reliability risk because the model may still try to answer when the retrieved context is weak. The prompt therefore tells the model to use only the context, cite chunk numbers, and say that it does not have enough information when the answer is missing.

## When I would use a managed vector database

I would consider switching from local ChromaDB to a managed vector database when the application has much higher traffic, needs automatic scaling, requires stronger availability guarantees, or when maintaining backups and infrastructure takes too much engineering time.
