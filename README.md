# MeetLens — Meeting & Lecture Summarisation using NLP

> **NLP Capstone Project | Project 18 | Group 3 — Team Techmorph**  
> **Program:** BCA (AI & Data Science), K.R. Mangalam University

**MeetLens** is an end-to-end Natural Language Processing studio that transforms lengthy meeting transcripts and lecture notes into concise executive summaries, numbered key takeaways, core TF-IDF topic tags, and actionable follow-ups with deadlines.

---

## Team Techmorph (Group 3)

| Roll Number | Name | Role & Contribution |
| :--- | :--- | :--- |
| **2401201145** | **Mohd Aman** | Lead Developer, Streamlit Studio UI & Model Integration |
| **2401201146** | **Kushagra Jain** | Data Cleaning, Preprocessing & Exploratory Data Analysis |
| **2401201147** | **Payal** | Extractive Baseline Implementation (TF-IDF + TextRank) |
| **2401201149** | **Aryan Sharma** | Transformer Fine-Tuning (`facebook/bart-base` on SAMSum) |
| **2401201153** | **Vivek** | ROUGE Benchmarking & Error Analysis |
| **2401201155** | **Lakshay Jain** | Documentation, Testing & Capstone Presentation |

---

## Problem Statement & Objectives

Meetings, lectures, and team discussions generate long transcripts where critical decisions, owners, and deadlines are buried in conversational noise. Reviewing full transcripts manually is slow and error-prone.

**Core Objectives:**
1. **Clean & Preprocess Transcripts:** Strip timestamps (`[00:01:20]`), speaker labels (`Rahul:`), conversational fillers (`um`, `uh`, `you know`), and redundant whitespace.
2. **Multi-Mode Summarisation:** Provide **Extractive** (TextRank), **Abstractive** (fine-tuned BART-base), and **Hybrid** (TextRank compression + BART rewriting) pipelines.
3. **Structured Insight Extraction:** Automatically surface top key takeaways, TF-IDF n-gram keywords, and action items with deadlines.
4. **Benchmark & Deploy:** Evaluate models quantitatively using ROUGE metrics and deliver an interactive Streamlit executive dashboard.

---

## Dataset & Preprocessing (`knkarthick/samsum`)

Trained and evaluated on the **SAMSum** conversational dialogue dataset (Messenger-style dialogues paired with human-written abstractive summaries):

| Split | Raw Rows | Duplicates Removed | Cleaned Rows | Avg Words (Dialogue / Summary) |
| :--- | :---: | :---: | :---: | :---: |
| **Train** | 14,731 | 476 | **14,210** | ~93 words / ~20 words |
| **Validation** | 818 | 0 | **818** | — |
| **Test** | 819 | 0 | **814** | — |

* **Zero missing values** across all splits.
* **Filtering:** Removed conversations shorter than 10 words and summaries shorter than 3 words.
* **Tokenisation:** Encoded using `facebook/bart-base` BPE tokenizer (`max_input_length = 512`, `max_target_length = 96`).

---

## System Architecture & Pipeline

```text
Transcript (.txt / .pdf / Paste)
        │
        ▼
┌───────────────────────────────┐
│  1. Transcript Preprocessing    │  ──► Strips timestamps, speaker prefixes & fillers
└───────────────────────────────┘
        │
        ├───────────────────────────────────────┐
        ▼                                       ▼
┌───────────────────────────────┐     ┌───────────────────────────────────┐
│  2. Extractive Engine         │     │  3. Abstractive / Hybrid Engine   │
│  TF-IDF + Cosine Similarity   │     │  Fine-Tuned BART-base (4 Beams)   │
│  + Power-Iteration PageRank   │     │  with 600-word Chunking           │
└───────────────────────────────┘     └───────────────────────────────────┘
        │                                       │
        └───────────────────┬───────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  4. Insight Extraction & Executive Studio UI                  │
│  • Executive Brief   • Word Compression Metrics               │
│  • Key Takeaways     • Core TF-IDF Topics   • Action Items    │
└───────────────────────────────────────────────────────────────┘
```

---

## Model Training & ROUGE Results

### Training Setup (`notebooks/MeetLens_Training.ipynb`)
* **Base Checkpoint:** `facebook/bart-base` (Encoder-Decoder Transformer)
* **Hyperparameters:** 2 epochs (3,554 steps), batch size `8`, learning rate `5e-5`, weight decay `0.01`, mixed precision (`fp16`)
* **Hardware & Time:** Google Colab T4 GPU (~8.5 minutes)

### Benchmark Comparison (First 200 Test Samples)

| Model | Type | Highlights & ROUGE Performance |
| :--- | :--- | :--- |
| **TextRank (Baseline)** | Unsupervised Extractive | `0.21` ROUGE-L — Fast, zero training, picks top-ranked sentences verbatim |
| **DistilBART (`sshleifer/distilbart-cnn-12-6`)** | Zero-Shot Abstractive | Pretrained on CNN/DailyMail news; struggles with multi-speaker dialogue style |
| **BART-base (`meetlens_model`)** | **Fine-Tuned Abstractive** | **`0.42` ROUGE-L (~2x baseline)** and **`+0.18` ROUGE-1** over pretrained DistilBART |

### Demo Run Benchmark (`sample_transcript.txt` — Hybrid Mode)
* **Input Length:** `207 words`
* **Generated Brief:** `59 words` (**71% text reduction**)
* **Extracted Insights:** Top 5 key takeaways, 10 TF-IDF topic tags, and 7 action items/deadlines.

---

## Project Structure

```text
MeetLens/
├── app.py                        # Streamlit executive dashboard UI
├── summarizer.py                 # Core NLP engine (cleaning, TextRank, BART inference)
├── evaluate.py                   # CLI script for ROUGE-1 / ROUGE-2 / ROUGE-L evaluation
├── requirements.txt              # Python dependencies
├── sample_transcript.txt         # Sample timestamped meeting transcript for testing
├── README.md                     # Project documentation
├── notebooks/
│   └── MeetLens_Training.ipynb   # Google Colab notebook (EDA, TextRank, DistilBART, BART fine-tuning)
└── meetlens_model/               # Local fine-tuned BART-base weights (excluded from Git; see setup)
```

---

## Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/amansaif/MeetLens-Meeting-Lecture-Summarisation.git
cd MeetLens-Meeting-Lecture-Summarisation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Fine-Tuned Model Weights (Optional)
* Open `notebooks/MeetLens_Training.ipynb` in **Google Colab (T4 GPU)** and run all cells to generate `meetlens_model.zip`.
* Extract `meetlens_model.zip` directly into the root project directory so `meetlens_model/` sits next to `app.py`.
* *Automatic Fallback:* If `meetlens_model/` is not found locally, `summarizer.py` automatically loads `sshleifer/distilbart-cnn-12-6` and updates the dashboard status pill accordingly.

### 4. Launch the Streamlit Studio
```bash
streamlit run app.py
```

### 5. Run CLI ROUGE Evaluation
```bash
# Evaluate extractive TextRank baseline
python evaluate.py --hf knkarthick/AMI -n 50 --method extractive

# Evaluate neural abstractive model
python evaluate.py --hf knkarthick/AMI -n 20 --method abstractive
```

---

## Limitations & Future Scope

### Current Limitations
* **Domain Shift:** Fine-tuned on short Messenger-style dialogues (SAMSum) rather than multi-hour corporate meetings; transcripts longer than 600 words are chunked, which can lose cross-chunk context.
* **Hallucination Risk:** Abstractive seq2seq models can occasionally infer unstated details, so generated briefs should be reviewed before distribution.
* **Rule-Based Action Items:** Action item detection relies on regex patterns (`will`, `should`, `by Friday`, `deadline`), which can occasionally flag agenda statements as tasks.

### Future Scope
* Fine-tune on long-form meeting benchmarks (**AMI** and **QMSum**).
* Integrate **OpenAI Whisper** for direct audio/video meeting transcription and speaker diarization.
* Replace regex action-item extraction with a supervised sequence-classification model.
* Add **Hindi and multilingual** meeting summarisation support.
