import re


class Chunk:
    def __init__(self, text, index):
        self.text = text
        self.chunk_index = index


def split_sentences(text):
    paragraphs = text.split("\n\n")
    sentences = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            parts = re.split(r"(?<=[.!?])\s+", paragraph)
            for sentence in parts:
                if sentence.strip():
                    sentences.append(sentence.strip())

    return sentences


def chunk_text(text, chunk_size, chunk_overlap):
    if chunk_overlap >= chunk_size:
        raise ValueError("Overlap should be smaller than chunk size")

    sentences = split_sentences(text)
    if len(sentences) == 0:
        return []

    chunks = []
    current_chunk = []
    current_length = 0
    i = 0

    while i < len(sentences):
        sentence = sentences[i]

        if current_length + len(sentence) > chunk_size and current_chunk:
            chunk_value = " ".join(current_chunk)
            chunks.append(Chunk(chunk_value, len(chunks)))

            overlap = []
            overlap_length = 0

            for old_sentence in reversed(current_chunk):
                if overlap_length + len(old_sentence) > chunk_overlap:
                    break
                overlap.insert(0, old_sentence)
                overlap_length += len(old_sentence)

            current_chunk = overlap
            current_length = overlap_length
        else:
            current_chunk.append(sentence)
            current_length += len(sentence) + 1
            i += 1

    if current_chunk:
        final_text = " ".join(current_chunk)
        chunks.append(Chunk(final_text, len(chunks)))

    return chunks
