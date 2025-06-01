from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SummaryRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(request: SummaryRequest):
    text = request.text.strip()
    if not text or len(text) < 10:
        return {"error": "Text too short to summarize."}
    
    # Dummy summary logic for now
    summary = text[:200] + "..."  # placeholder
    return {"summary": summary}
