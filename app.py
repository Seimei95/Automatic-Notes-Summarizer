from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

class SummaryRequest(BaseModel):
    text: str

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


@app.post("/summarize")
def summarize(request: SummaryRequest):
    text = request.text.strip()
    if not text or len(text) < 10:
        return {"error": "Text too short to summarize."}
    try:
        summary = summarizer(text, max_length=180, min_length=30, do_sample=False)
        return {"summary": summary[0]["summary_text"]}
    except Exception as e:
        return {"error": "Summarization failed", "details": str(e)}

