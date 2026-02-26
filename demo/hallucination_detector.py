def detect_hallucinations(text):
    """
    Detects potential hallucinated content in a given text.
    A hallucination in this context refers to statements or information presented as fact but not based on reliable sources.
    """
    # Example criterion for detecting hallucinations
    hallucination_indicators = [
        "claims to be", 
        "according to sources", 
        "experts say", 
        "research has shown"
    ]

    for indicator in hallucination_indicators:
        if indicator in text.lower():
            return f"Potential hallucination detected: {indicator} found in text."
    return "No hallucinations detected."

if __name__ == "__main__":
    sample_text = "This product claims to be the best according to sources that aren't specified."
    result = detect_hallucinations(sample_text)
    print(result)