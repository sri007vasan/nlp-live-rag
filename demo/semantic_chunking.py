import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class SemanticChunking:
    def __init__(self, min_chunk_size=100):
        self.min_chunk_size = min_chunk_size
        self.vectorizer = TfidfVectorizer()

    def chunk_text(self, text):
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = []

        for sentence in sentences:
            current_chunk.append(sentence)
            if len(' '.join(current_chunk)) >= self.min_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def get_semantic_chunks(self, text):
        chunks = self.chunk_text(text)
        tfidf_matrix = self.vectorizer.fit_transform(chunks)
        cosine_sim = cosine_similarity(tfidf_matrix)

        semantic_chunks = []
        for i, chunk in enumerate(chunks):
            if i == 0 or np.max(cosine_sim[i-1]) < 0.5:
                semantic_chunks.append(chunk)

        return semantic_chunks

# Example usage:
# text = "Your document text goes here."  # Replace with actual text
# chunker = SemanticChunking()
# semantic_chunks = chunker.get_semantic_chunks(text)
# print(semantic_chunks)