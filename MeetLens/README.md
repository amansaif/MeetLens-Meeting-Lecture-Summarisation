# MeetLens - Meeting & Lecture Summarisation (NLP Capstone, Project 18)
Team Techmorph - K.R. Mangalam University

## Features
- Transcript cleaning (timestamps, speaker labels, filler words)
- **Extractive** summary: TF-IDF + TextRank
- **Abstractive** summary: DistilBART (HuggingFace) with chunking for long text
- **Hybrid** mode (TextRank compression -> DistilBART)
- Key points, keywords, action-item detection
- Streamlit GUI: paste/upload (.txt/.pdf), summary length slider, download

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Evaluation (ROUGE)
```bash
python evaluate.py --hf knkarthick/AMI -n 50 --method extractive
python evaluate.py --hf knkarthick/AMI -n 20 --method abstractive
```

## Project structure
- `summarizer.py` - NLP pipeline
- `app.py` - Streamlit GUI
- `evaluate.py` - ROUGE evaluation
- `notebooks/MeetLens_Training.ipynb` - Colab notebook (cleaning, EDA, TextRank baseline, fine-tuning BART, ROUGE). Unzip the downloaded `meetlens_model.zip` next to `app.py` and the app uses it automatically.
- `sample_transcript.txt` - demo input

## Limitations
Abstractive models can hallucinate; action items are rule-based; long transcripts are chunked so cross-chunk context is lost.
