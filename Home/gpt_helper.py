import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# ✅ Configure Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def select_best_questions(user_intro):
    prompt = f"""
    Based on the following self-introduction, generate 5 short personality assessment questions. 
    Avoid yes/no questions, and make them behavior-focused. Provide each question on a new line.
    
    Introduction: "{user_intro}"
    
    Questions:
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    questions_text = response.text.strip()
    questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
    return questions


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
