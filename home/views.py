from django.shortcuts import render
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def chatbot_view(request):
    return render(request, 'index.html')

genai.configure(api_key="YOUR_API_KEY")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="precise and concise outputs",
)

@csrf_exempt
@require_POST
def ask_question(request):
    question = request.POST.get("question")
    if not question:
        return JsonResponse({"error": "Question is required"}, status=400)

    chat_session = model.start_chat(history=[{"role": "user", "parts": [question]}])
    response = chat_session.send_message(question)

    return JsonResponse({"answer": response.text})