"""MeetLens - core NLP engine for Meeting / Lecture summarisation.

Pipeline: clean -> sentence split -> TF-IDF -> TextRank (extractive)
          -> optional BART/DistilBART (abstractive) -> key points + action items.
"""
import os
import re
import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

FILLERS = r"\b(um+|uh+|erm|hmm+|you know|i mean|kind of|sort of)\b,?"
TIMESTAMP = r"[\[\(]?\d{1,2}:\d{2}(?::\d{2})?[\]\)]?"
SPEAKER = r"^\s*[A-Z][A-Za-z .]{0,25}:\s*"

ACTION_PATTERNS = [
    r"\baction item\b", r"\bto[- ]?do\b", r"\bneed(s)? to\b", r"\bhas to\b", r"\bhave to\b",
    r"\bshould\b", r"\bmust\b", r"\bwill (send|prepare|share|complete|finish|submit|review|update|check|create|call|set up|schedule|follow)\b",
    r"\bplease\b", r"\blet'?s\b", r"\bassign(ed)?\b", r"\bdeadline\b", r"\bfollow[- ]?up\b",
    r"\bby (monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|next week|end of (the )?(day|week|month))\b",
    r"\bi'll\b", r"\bwe'll\b",
]
ACTION_RE = re.compile("|".join(ACTION_PATTERNS), re.I)


def clean_transcript(text: str) -> str:
    """Remove timestamps, speaker labels, filler words, extra spaces."""
    lines = []
    for ln in text.splitlines():
        ln = re.sub(TIMESTAMP, " ", ln)
        ln = re.sub(SPEAKER, "", ln)
        lines.append(ln)
    text = " ".join(lines)
    text = re.sub(FILLERS, " ", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text: str):
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text)
    return [s.strip() for s in sents if len(s.split()) >= 4]


def textrank_scores(sentences, damping=0.85, iters=60):
    """TF-IDF sentence vectors -> cosine similarity graph -> PageRank (power iteration)."""
    if len(sentences) < 2:
        return np.ones(len(sentences))
    vec = TfidfVectorizer(stop_words="english")
    try:
        X = vec.fit_transform(sentences)
    except ValueError:
        return np.ones(len(sentences))
    sim = cosine_similarity(X)
    np.fill_diagonal(sim, 0)
    row = sim.sum(axis=1, keepdims=True)
    row[row == 0] = 1
    M = sim / row
    n = len(sentences)
    r = np.ones(n) / n
    for _ in range(iters):
        r = (1 - damping) / n + damping * M.T @ r
    return r


def extractive_summary(text: str, num_sentences: int = 5):
    sents = split_sentences(clean_transcript(text))
    if not sents:
        return [], []
    scores = textrank_scores(sents)
    k = min(num_sentences, len(sents))
    top = sorted(np.argsort(scores)[::-1][:k])  # keep original order
    return [sents[i] for i in top], sents


def extract_keywords(text: str, top_n: int = 10):
    sents = split_sentences(clean_transcript(text))
    if not sents:
        return []
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=500)
    X = vec.fit_transform(sents)
    scores = np.asarray(X.sum(axis=0)).ravel()
    terms = np.array(vec.get_feature_names_out())
    return list(terms[np.argsort(scores)[::-1][:top_n]])


def extract_action_items(text: str, max_items: int = 10):
    sents = split_sentences(clean_transcript(text))
    items = [s for s in sents if ACTION_RE.search(s)]
    return items[:max_items]


_ABS = {}

# Agar app.py ke paas 'meetlens_model' folder hai toh fine-tuned model use hoga, warna pretrained
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_MODEL_DIR = os.path.join(BASE_DIR, "meetlens_model")
DEFAULT_MODEL = LOCAL_MODEL_DIR if os.path.isdir(LOCAL_MODEL_DIR) else "sshleifer/distilbart-cnn-12-6"


def abstractive_summary(text: str, max_len: int = 120, min_len: int = 30,
                        model: str = DEFAULT_MODEL):
    """Transformer seq2seq summary. Long text is chunked (~600 words) then merged."""
    if model not in _ABS:
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        tok = AutoTokenizer.from_pretrained(model)
        mod = AutoModelForSeq2SeqLM.from_pretrained(model).to(dev)
        mod.eval()
        _ABS[model] = (tok, mod, dev)

    tok, mod, dev = _ABS[model]
    words = clean_transcript(text).split()
    chunks = [" ".join(words[i:i + 600]) for i in range(0, len(words), 600)]
    parts = []
    for c in chunks:
        if len(c.split()) < 40:
            parts.append(c)
            continue
        inputs = tok(c, max_length=512, truncation=True, return_tensors="pt").to(dev)
        with torch.no_grad():
            summary_ids = mod.generate(
                **inputs,
                max_length=max_len,
                min_length=min(min_len, max_len - 10),
                do_sample=False,
                num_beams=4,
                early_stopping=True
            )
        parts.append(tok.decode(summary_ids[0], skip_special_tokens=True))
    return " ".join(parts)


def summarize(text: str, method: str = "extractive", num_sentences: int = 5):
    """method: 'extractive' | 'abstractive' | 'hybrid'"""
    ext, _ = extractive_summary(text, num_sentences)
    if method == "extractive":
        summary = " ".join(ext)
    elif method == "abstractive":
        summary = abstractive_summary(text)
    else:  # hybrid: compress with TextRank first, then rewrite with transformer
        compressed, _ = extractive_summary(text, max(num_sentences * 3, 10))
        summary = abstractive_summary(" ".join(compressed))
    return {
        "summary": summary,
        "key_points": ext,
        "keywords": extract_keywords(text),
        "action_items": extract_action_items(text),
        "orig_words": len(text.split()),
        "summ_words": len(summary.split()),
    }