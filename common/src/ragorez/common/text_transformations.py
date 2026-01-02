import re


def delete_spaces_and_new_lines(text):
    """remove excess spaces and new lines"""
    text = re.sub(r"\.{2,}", "", text)
    text = re.sub(r"\n+", ".", text)
    text = re.sub(r" +", " ", text)
    text = text.strip()
    return text


def transform_to_chunks(text: str, chunk_size, overlap):
    """creates chunks from text with overlap"""
    sentences = (i.strip() for i in re.split(r"[.!?]\s+", text))
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
                if len(prev_chunk) <= overlap:
                    overlap_text = prev_chunk
                else:
                    last_part = prev_chunk[-overlap:]
                    first_dot = last_part.find('. ')
                    if first_dot != -1:
                        overlap_text = last_part[first_dot + 1:].strip()
                    else:
                        overlap_text = last_part
                current_chunk = overlap_text + " " + sentence + " "
            else:
                current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
