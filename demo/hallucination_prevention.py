import logging
import re
import numpy as np
import nltk
from sklearn.metrics.pairwise import cosine_similarity

# Define a class for Hallucination Prevention
class HallucinationPrevention:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        nltk.download('punkt')  # Download necessary NLTK resources

    def detect_hallucination(self, generated_text, reference_text):
        # Simple keyword matching for hallucination detection
        keywords = set(re.findall(r'\b\w+\b', reference_text.lower()))
        generated_words = set(re.findall(r'\b\w+\b', generated_text.lower()))
        hallucinated_words = generated_words - keywords
        if hallucinated_words:
            logging.warning('Detected potential hallucinated words: {}'.format(hallucinated_words))
            return True  # Hallucination detected
        return False  # No hallucination

    def cosine_similarity_check(self, generated_embedding, reference_embedding):
        # Calculate cosine similarity to detect hallucination
        similarity = cosine_similarity([generated_embedding], [reference_embedding])[0][0]
        if similarity < 0.7:  # Threshold
            logging.warning('Low similarity detected. Potential hallucination.')
            return True
        return False

    def layered_detection(self, generated_text, reference_text, generated_embedding, reference_embedding):
        if self.detect_hallucination(generated_text, reference_text):
            return True
        if self.cosine_similarity_check(generated_embedding, reference_embedding):
            return True
        return False

    def prevent_hallucination(self, generated_text, reference_text, generated_embedding, reference_embedding):
        if self.layered_detection(generated_text, reference_text, generated_embedding, reference_embedding):
            logging.info('Hallucination detected. Taking preventive measures.')
            # Implement preventive measures like re-generating text
            return self.regenerate_text(reference_text)
        logging.info('No hallucination detected.')
        return generated_text

    def regenerate_text(self, reference_text):
        # Placeholder for text generation logic
        logging.info('Regenerating text based on reference.')
        return reference_text  # Simplification for demo purposes

# Example usage
if __name__ == '__main__':
    hp = HallucinationPrevention()
    # Dummy data for demonstration
    generated = "The eagle flies over the rainbow"  # This should trigger prevention
    reference = "The eagle is a bird known for its strength."
    generated_embedding = np.random.rand(768)  # Dummy embedding
    reference_embedding = np.random.rand(768)  # Dummy embedding
    result = hp.prevent_hallucination(generated, reference, generated_embedding, reference_embedding)
    print(result)  # Output the result