def process_text(text):
    if not text or len(text) < 3:
        raise ValueError("Text input must be meaningful.")
    return text.lower()
