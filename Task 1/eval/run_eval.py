import json
import os
import statistics
import time

from eval.answer_metrics import exact_match, f1_score, judge_answer
from eval.cost_model import build_cost_table
from eval.retrieval_metrics import recall_at_k, mrr, ndcg_at_k, average
from src.embed import embed_texts
from src.store import search_chunks, count_chunks
from src.generate import generate_answer


def retrieve_for_eval(question, top_k):
    embedding = embed_texts([question])[0]
    result = search_chunks(embedding, top_k)

    texts = result["documents"][0]
    metadatas = result["metadatas"][0]

    source_docs = []
    for metadata in metadatas:
        source_docs.append(metadata.get("source_doc"))

    return texts, source_docs


def run_eval():
    if count_chunks() == 0:
        print("Vector database is empty. Ingest sample_docs first.")
        return

    file = open("eval/qa_dataset.json", "r", encoding="utf-8")
    questions = json.load(file)
    file.close()

    top_k = 3
    results = []
    recall_scores = []
    mrr_scores = []
    ndcg_scores = []
    f1_scores = []
    em_scores = []
    faithfulness_scores = []
    relevance_scores = []
    latencies = []

    for item in questions:
        start = time.time()

        chunks, retrieved_docs = retrieve_for_eval(item["question"], top_k)
        answer, input_tokens, output_tokens = generate_answer(item["question"], chunks)

        latency = (time.time() - start) * 1000
        latencies.append(latency)

        relevant_docs = item["relevant_source_docs"]
        no_answer = item["gold_answer"] == "NO_ANSWER"

        row = {
            "id": item["id"],
            "question": item["question"],
            "answer": answer,
            "retrieved_docs": retrieved_docs,
            "latency_ms": round(latency, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }

        if no_answer:
            row["correctly_declined"] = "don't have enough information" in answer.lower()
        else:
            recall = recall_at_k(retrieved_docs, relevant_docs, top_k)
            reciprocal_rank = mrr(retrieved_docs, relevant_docs)
            ndcg = ndcg_at_k(retrieved_docs, relevant_docs, top_k)
            em = exact_match(answer, item["gold_answer"])
            f1 = f1_score(answer, item["gold_answer"])

            context = "\n\n".join(chunks)
            judge = judge_answer(item["question"], context, answer)

            row["recall_at_k"] = recall
            row["mrr"] = reciprocal_rank
            row["ndcg_at_k"] = ndcg
            row["exact_match"] = em
            row["f1"] = f1
            row["faithfulness"] = judge.get("faithfulness")
            row["relevance"] = judge.get("relevance")

            recall_scores.append(recall)
            mrr_scores.append(reciprocal_rank)
            ndcg_scores.append(ndcg)
            em_scores.append(em)
            f1_scores.append(f1)

            if row["faithfulness"] is not None:
                faithfulness_scores.append(row["faithfulness"])
            if row["relevance"] is not None:
                relevance_scores.append(row["relevance"])

        results.append(row)

    summary = {
        "questions": len(questions),
        "top_k": top_k,
        "recall_at_k": round(average(recall_scores), 3),
        "mrr": round(average(mrr_scores), 3),
        "ndcg_at_k": round(average(ndcg_scores), 3),
        "exact_match": round(average(em_scores), 3),
        "f1": round(average(f1_scores), 3),
        "faithfulness": round(average(faithfulness_scores), 3) if faithfulness_scores else None,
        "relevance": round(average(relevance_scores), 3) if relevance_scores else None,
        "latency_mean_ms": round(statistics.mean(latencies), 2) if latencies else 0,
        "latency_median_ms": round(statistics.median(latencies), 2) if latencies else 0,
        "cost_table": build_cost_table()
    }

    output = {
        "summary": summary,
        "results": results
    }

    os.makedirs("results", exist_ok=True)
    output_file = open("results/eval_results.json", "w", encoding="utf-8")
    json.dump(output, output_file, indent=2)
    output_file.close()

    print(json.dumps(summary, indent=2))
    print("Evaluation saved to results/eval_results.json")


if __name__ == "__main__":
    run_eval()
