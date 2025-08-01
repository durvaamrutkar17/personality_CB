import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (API key)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")
genai.configure(api_key=api_key)


# ✅ Generate dynamic multiple-choice questions
def select_best_questions(user_intro):
    prompt = f"""
    Based on the following user intro: "{user_intro}", generate 2 personality assessment questions.
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

    # Remove markdown code block if present
    if raw.startswith("```json") or raw.startswith("```"):
        raw = raw.strip("`")
        raw = "\n".join(line for line in raw.splitlines() if not line.strip().startswith("json"))

    # Try to parse JSON
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("❌ Gemini returned malformed JSON:\n\n" + raw) from e


# ✅ Generate a full personality profile based on all answers
def generate_personality_profile(user_intro, qa_pairs):
    questions_formatted = "\n".join([f"{i+1}. Q: {q}\nA: {a}" for i, (q, a) in enumerate(qa_pairs)])
    
    prompt = f"""
    Based on the following introduction and answers, identify the user's dominant personality type in ONE WORD.
    Then, provide a short personality profile (3-4 sentences).
    Also list 2-3 strengths (Pros) and 2-3 limitations (Cons) of this personality type.

    Introduction: "{user_intro}"
    Answers:
    {questions_formatted}

    Format the response like this:

    Personality Type: <One Word>

    Pros:
    - <Positive trait 1>
    - <Positive trait 2>
    - <Optional positive trait 3>

    Cons:
    - <Limitation 1>
    - <Limitation 2>
    - <Optional limitation 3>

    Profile: <3-4 sentence paragraph>
    """
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()



# ✅ Generate a friendly one-liner after each question answer
def generate_feedback(question, answer):
    prompt = f"""
    A user responded to a personality question.

    Q: {question}
    A: {answer}

    Write a short, friendly, empathetic, and informal 1-line response as a personality chatbot. Make it warm and encouraging.
    Example: "That's a great way to handle things!" or "Sounds like you’re someone who values honesty!"
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    # print(response)
    return response.text.strip()
