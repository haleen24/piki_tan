import re


class Cleaner:
    def clean(self, text: str) -> str:
        pass


class DefaultRegexpCleaner(Cleaner):
    def clean(self, text: str) -> str:
        return clean_text(text)


def clean_text(text):
    """Очищает текст от лишних пробелов и переносов"""
    text = re.sub(r"\.{2,}", "", text)
    text = re.sub(r"\n+", "", text)
    text = re.sub(r" +", " ", text)
    text = text.strip()
    return text


class Transformator:
    def get_chunks(text: str) -> list[str]:
        pass


class DefaultTransformator(Transformator):
    def __init__(self, chunk_size, overlap):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def get_chunks(self, text: str) -> list[str]:
        return transform_to_chunks(text, self.chunk_size, self.overlap)


def transform_to_chunks(text: str, chunk_size, overlap):
    """Разбивает текст на чанки с перекрытием"""
    sentences = re.split(r"[.!?]\s+", text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if overlap > 0 and chunks:
                prev_chunk = chunks[-1]
                overlap_text = (
                    prev_chunk[-overlap:] if len(prev_chunk) > overlap else prev_chunk
                )
                current_chunk = overlap_text + " " + sentence + " "
            else:
                current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
