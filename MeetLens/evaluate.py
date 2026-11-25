"""Evaluate summariser with ROUGE.
Usage:
  python evaluate.py --csv data.csv            # columns: transcript,summary
  python evaluate.py --hf knkarthick/AMI -n 50 # HF dataset with dialogue/summary columns
  add --method abstractive  to test the transformer
"""
import argparse
import pandas as pd
from rouge_score import rouge_scorer
from summarizer import summarize

ap = argparse.ArgumentParser()
ap.add_argument("--csv")
ap.add_argument("--hf")
ap.add_argument("-n", type=int, default=50)
ap.add_argument("--method", default="extractive")
ap.add_argument("--sents", type=int, default=5)
a = ap.parse_args()

if a.csv:
    df = pd.read_csv(a.csv)
    X, Y = df["transcript"].tolist(), df["summary"].tolist()
else:
    from datasets import load_dataset
    ds = load_dataset(a.hf, split="test")
    X, Y = ds["dialogue"], ds["summary"]
X, Y = X[:a.n], Y[:a.n]

sc = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
tot = {"rouge1": 0, "rouge2": 0, "rougeL": 0}
for x, y in zip(X, Y):
    p = summarize(x, a.method, a.sents)["summary"]
    s = sc.score(y, p)
    for k in tot:
        tot[k] += s[k].fmeasure
print(f"Method: {a.method} | samples: {len(X)}")
for k, v in tot.items():
    print(f"{k}: {v / len(X):.4f}")
