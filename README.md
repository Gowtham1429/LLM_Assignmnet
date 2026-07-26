# LLM Engineering Assignment

This repository contains two tasks related to Retrieval-Augmented Generation (RAG) and LLM evaluation.

## Task 1 - RAG Application

Task 1 implements a simple Retrieval-Augmented Generation pipeline.

### Features

- Supports PDF, HTML, and Markdown documents
- Extracts text from documents
- Splits text into chunks with overlap
- Generates embeddings using Sentence Transformers
- Stores embeddings in ChromaDB
- Uses unique chunk IDs to avoid duplicate vectors during re-ingestion
- Stores metadata such as source document and document type
- Supports metadata-based filtering
- Retrieves relevant chunks for a user question
- Generates answers using retrieved context
- Tracks query latency, chunk count, input tokens, and output tokens
- Stores query information in a JSONL log file
- Includes evaluation for retrieval and answer quality

### Technologies

- Python
- ChromaDB
- Sentence Transformers
- Anthropic API
- BeautifulSoup
- PyPDF

---

## Task 2 - LLM-as-Judge Evaluation Pipeline

Task 2 implements an LLM-based evaluation pipeline for comparing model responses.

### Features

- Reads test cases from JSON
- Uses a structured evaluation rubric
- Scores responses from 1 to 5
- Evaluates:
  - Correctness
  - Faithfulness
  - Completeness
  - Instruction following
  - Tone
  - Safety
- Supports A-vs-B answer comparison
- Uses reference-based evaluation
- Checks position bias by running both A/B and B/A order
- Measures position flip rate
- Logs judge prompts and raw responses
- Tracks judge input and output tokens
- Compares judge decisions with gold labels
- Generates a final JSON evaluation report

### Bias Handling

The evaluation pipeline considers common LLM judge biases.

**Position Bias:**  
Each comparison is performed in both A/B and B/A order. If the final winner changes after swapping positions, it is counted as a position flip.

**Verbosity Bias:**  
The judge is instructed not to prefer an answer simply because it is longer.

**Style and Sycophancy Bias:**  
The judge is instructed to focus on correctness and the reference answer instead of confidence or writing style.

**Self-Enhancement Bias:**  
The judge model can be configured independently from the model that generated the responses.

**Score Clustering:**  
Instead of using only one overall score, separate criteria are scored with a reason for each score.

---

## Project Structure

    LLM_Assignment/
    |
    |-- Task 1/
    |   |-- src/
    |   |-- eval/
    |   |-- sample_docs/
    |   |-- README.md
    |   |-- requirements.txt
    |
    |-- Task 2/
        |-- src/
        |-- data/
        |-- logs/
        |-- results/
        |-- main.py
        |-- README.md
        |-- requirements.txt

## Setup

Clone the repository:

    git clone <repository-url>

Install the required packages separately for each task:

    pip install -r requirements.txt

Set the Anthropic API key as an environment variable.

Windows PowerShell:

    $env:ANTHROPIC_API_KEY="your_api_key"

Linux/macOS:

    export ANTHROPIC_API_KEY=your_api_key

The API key is not stored directly in the source code.

## Running the Projects

For Task 1, follow the instructions available inside the Task 1 README to ingest documents and query the RAG system.

For Task 2:

    cd "Task 2"
    python main.py

The evaluation results are saved in the results folder and judge calls are recorded in the logs folder.

## Models

**Embedding Model:** all-MiniLM-L6-v2

**Judge Model:** Claude Sonnet 4.5

The judge model is configurable through environment variables.

## Author

Sai Gowtham
