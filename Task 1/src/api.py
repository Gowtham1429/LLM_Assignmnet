from fastapi import FastAPI
from pydantic import BaseModel

from src.retrieve import retrieve
from src.generate import generate_answer

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3


@app.post("/query")
def query(request: QuestionRequest):
    chunks = retrieve(request.question, request.top_k)
    answer, input_tokens, output_tokens = generate_answer(request.question, chunks)

    return {
        "answer": answer,
        "chunks_used": len(chunks),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }
