from fastapi import FastAPI, Query
from typing import List
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# FastAPI app
app = FastAPI()

@app.get("/generate_cv")
def generate_cv(
    name: str = Query(...),
    experience: str = Query(...),
    education: str = Query(...),
    tech_stack: List[str] = Query(...)
):
    prompt = f"""
You are a CV assistant. Generate a JSON CV for the following person:

Name: {name}
Experience: {experience}
Education: {education}
Tech stack: {', '.join(tech_stack)}

Format:
{{
  "name": "Person Name",
  "intro": "...short self-intro...",
  "experience": "...detailed...",
  "education": "...detailed...",
  "tech_stack": ["...", "..."],
  "summary": "...summary of strengths...",
  "wishes": "...kind letter, what the person wants to find in the company ..."
}}

Output only valid JSON. Dont imagine anything, only facts from user.
Send json as raw text without markdown(without ```json...)
    """

    response = model.generate_content(prompt)
    try:
        return response.text.strip()
    except Exception as e:
        return {"error": str(e)}
