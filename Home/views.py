import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .gpt_helper import select_best_questions, generate_personality_profile

@csrf_exempt  # Optional: for testing POST without CSRF token
def index(request):
    if request.method == 'POST':
        user_intro = request.POST.get('intro', '')
        qa_data = select_best_questions(user_intro)
        questions = [q["question"] for q in qa_data]
        options = [q["options"] for q in qa_data]


        # Ensure questions is a list of clean sentences
        if isinstance(questions, str):
            split_by_numbering = re.split(r'\d+\.\s*', questions)
            cleaned_questions = [q.strip() for q in split_by_numbering if len(q.strip()) > 5]
            if len(cleaned_questions) > 1:
                questions = cleaned_questions
            else:
                questions = [q.strip() for q in questions.split('.') if len(q.strip()) > 5]

        
        return render(request, 'index.html', {
            'intro': user_intro,
            'questions': questions,
            'options': options
        })


    return render(request, 'index.html', {
        'intro': None,
        'questions': None
    })

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        user_intro = request.POST.get('intro', '')
        questions = request.POST.getlist('questions')
        answers = [request.POST.get(f'answer_{i}', '') for i in range(len(questions))]
        qa_pairs = list(zip(questions, answers))
        profile = generate_personality_profile(user_intro, qa_pairs)

        return render(request, 'index.html', {
            'intro': user_intro,
            'profile': profile
        })
    return render(request, 'index.html')
