
import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import nltk

# Safe downloader
for pkg in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.download(pkg, quiet=True)
    except:
        pass


# Download required NLTK data silently
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

def summarize_text(text, compression_ratio=0.5):
    """
    Offline extractive summarizer.
    Keeps all key ideas while reducing redundant phrases.
    Works without transformers or internet access.
    """

    # Clean and validate input
    if not text or len(text.strip()) < 50:
        return text.strip()

    # Split text into sentences
    sentences = sent_tokenize(text)
    if len(sentences) <= 3:
        return text.strip()

    # Tokenize and remove stopwords
    words = [w.lower() for w in word_tokenize(text) if w.isalpha()]
    stop_words = set(stopwords.words("english"))

    # Compute word frequency
    freq = {}
    for w in words:
        if w not in stop_words:
            freq[w] = freq.get(w, 0) + 1

    # Normalize word frequency
    max_freq = max(freq.values()) if freq else 1
    for w in freq:
        freq[w] /= max_freq

    # Score sentences based on word importance
    sentence_scores = {}
    for sent in sentences:
        sent_words = [w.lower() for w in word_tokenize(sent) if w.isalpha()]
        if not sent_words:
            continue
        # Weight sentences by average of word frequencies
        score = sum(freq.get(w, 0) for w in sent_words) / len(sent_words)
        # Slightly boost sentences with key connectors (context)
        if any(kw in sent.lower() for kw in ["because", "however", "but", "although", "therefore"]):
            score *= 1.1
        sentence_scores[sent] = score

    # Select top N sentences based on compression ratio
    num_sentences = max(3, math.ceil(len(sentences) * compression_ratio))
    ranked = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

    # Preserve original order for readability
    final_summary = [s for s in sentences if s in ranked]

    # Join into one text block
    summary = " ".join(final_summary)

    # Post-process: ensure it’s not too short or choppy
    if len(summary.split()) < 50:
        summary += " " + sentences[-1]

    return summary.strip()
