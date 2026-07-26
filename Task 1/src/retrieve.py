from src.embed import embed_texts
from src.store import search_chunks


def retrieve(question, top_k=3, doc_type=None):
    question_embedding = embed_texts([question])
    query_embedding = question_embedding[0]

    result = search_chunks(query_embedding, top_k, doc_type)
    documents = result["documents"][0]

    chunks = []
    for document in documents:
        chunks.append(document)

    return chunks
