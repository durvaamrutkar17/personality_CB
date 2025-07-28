from django.shortcuts import render
from .gpt_helper import get_gemini_astrology

def astro(request):
    response = None
    if request.method == "POST":
        dob = request.POST.get("dob")
        tob = request.POST.get("tob")
        place = request.POST.get("place")

        prompt = f"""
            Give an astrological analysis based on:
            Date of Birth: {dob}
            Time of Birth: {tob}
            Place of Birth: {place}

            Respond in clear, numbered bullet points.
            Add a line break after each point for readability.
            Each point should be short and insightful.
        """

        response = get_gemini_astrology(prompt)

    return render(request, "astro.html", {"response": response})
