from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

app = FastAPI()

# what feedback we have received
class Review(BaseModel):
    text: str

class Analysis(BaseModel):
    label: str     #"Positive", "Negative", or  "Neutral"
    score: int     #1 (very bad) to 5 (very good)
    theme: str  # Category, mainly on which the review is about

@app.post("/analyze")
def analyze(review: Review):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=(
            "Analyze this customer review.\n"
            "label must be 'positive', 'negative', or 'neutral'.\n"
            "score must be a number from 1 (very bad) to 5 (very good).\n"
            "theme must be ONE lowercase word for the main topic "
            "(for example: delivery, taste, price, service, quality).\n"
            f"Review: {review.text}"
        ),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Analysis,
        ),
    )
    return response.parsed


