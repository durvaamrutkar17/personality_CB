import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")
genai.configure(api_key=api_key)


def select_best_questions(user_intro):
    prompt = f"""
    Based on the following user intro: "{user_intro}", generate 10 personality assessment questions.
    For each question, include 4 multiple-choice options.

    Output ONLY a valid JSON array like this:
    [
      {{
        "question": "How do you handle stress?",
        "options": ["Stay calm", "Express emotions", "Isolate", "Distract myself"]
      }},
      ...
    ]

    Do NOT add any commentary or markdown (no ```json or explanation).
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # ✅ Remove markdown code block if present
    if raw.startswith("```json") or raw.startswith("```"):
        raw = raw.strip("`")  # removes all backticks
        raw = "\n".join(line for line in raw.splitlines() if not line.strip().startswith("json"))

    # ✅ Print for debugging
    print("🔍 Gemini response (cleaned):")
    

    # ✅ Try to parse JSON
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("❌ Gemini returned malformed JSON:\n\n" + raw) from e




def generate_personality_profile(user_intro, qa_pairs):
    questions_formatted = "\n".join([f"{i+1}. Q: {q}\nA: {a}" for i, (q, a) in enumerate(qa_pairs)])
    prompt = f"""
    Based on the following introduction and answers, write a concise personality profile in 4-5 sentences.
    
    Introduction: "{user_intro}"
    Answers:
    {questions_formatted}
    
    Personality Profile:
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()
