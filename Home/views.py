import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .gpt_helper import (
    select_best_questions,
    generate_personality_profile,
    generate_feedback
)
from .models import personalityResponse
@csrf_exempt
def index(request):
    if request.method == 'POST':
        user_intro = request.POST.get('intro', '')
        qa_data = select_best_questions(user_intro)
        questions = [q["question"] for q in qa_data]
        options = [q["options"] for q in qa_data]

        # Clean malformed question formatting if needed
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
        personalityResponse.objects.create(
            user=request.user,  
            response=profile
        )
        return render(request, 'index.html', {
            'intro': user_intro,
            'profile': profile
        })

    return render(request, 'index.html')


@csrf_exempt
def feedback_view(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        try:
            feedback = generate_feedback(question, answer)
            # print("✅ Feedback:", feedback)  # Optional debug
            return JsonResponse({'feedback': feedback})
        except Exception as e:
            print("❌ Gemini Feedback Error:", str(e))
            return JsonResponse({'feedback': "Thanks for your answer!"})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
