import hashlib
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")


def make_id(source_doc, chunk_index, text):
    data = source_doc + str(chunk_index) + text
    chunk_id = hashlib.sha256(data.encode()).hexdigest()
    return chunk_id


def store_chunks(source_doc, doc_type, texts, embeddings):
    ids = []
    metadatas = []

    for i in range(len(texts)):
        chunk_id = make_id(source_doc, i, texts[i])
        ids.append(chunk_id)
        metadatas.append({
            "source_doc": source_doc,
            "doc_type": doc_type,
            "chunk_index": i
        })

    existing_ids = []

    if len(ids) > 0:
        result = collection.get(ids=ids)
        existing_ids = result["ids"]

    new_ids = []
    new_texts = []
    new_embeddings = []
    new_metadatas = []

    for i in range(len(ids)):
        if ids[i] not in existing_ids:
            new_ids.append(ids[i])
            new_texts.append(texts[i])
            new_embeddings.append(embeddings[i])
            new_metadatas.append(metadatas[i])

    if len(new_ids) > 0:
        collection.add(
            ids=new_ids,
            documents=new_texts,
            embeddings=new_embeddings,
            metadatas=new_metadatas
        )

    new_count = len(new_ids)
    existing_count = len(ids) - new_count
    return new_count, existing_count


def search_chunks(query_embedding, top_k=3, doc_type=None):
    where = None

    if doc_type:
        where = {"doc_type": doc_type}

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where
    )
    return result


def count_chunks():
    return collection.count()
