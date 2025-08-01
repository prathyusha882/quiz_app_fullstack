from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.response import TemplateResponse

from .forms import GenerateQuestionsForm
from .models import Question, Option, Quiz
# from .ollama_client import generate_questions_with_ollama  # Temporarily commented out
# import requests  # Temporarily commented out

# -------------------------------
# Question Admin (Basic + Prompt View)
# -------------------------------

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-questions/', self.admin_site.admin_view(self.generate_questions_view), name='generate-questions'),
        ]
        return custom_urls + urls

    def generate_questions_view(self, request):
        if request.method == 'POST':
            form = GenerateQuestionsForm(request.POST)
            if form.is_valid():
                quiz = form.cleaned_data['quiz']
                prompt = form.cleaned_data['prompt']

                try:
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "llama3",
                            "prompt": prompt,
                            "stream": False
                        },
                        timeout=60
                    )

                    if response.status_code == 200:
                        ai_text = response.json().get("response", "")
                        created = self.save_questions_from_text(ai_text, quiz)
                        messages.success(request, f"{created} questions generated and saved to quiz '{quiz.title}'.")
                        return redirect("..")
                    else:
                        messages.error(request, f"Ollama Error: {response.text}")
                except Exception as e:
                    messages.error(request, f"Connection Error: {e}")
        else:
            form = GenerateQuestionsForm()

        return render(request, "admin/generate_questions_form.html", {"form": form})

    def save_questions_from_text(self, text, quiz):
        created_count = 0
        questions = text.split("Q")
        for q in questions:
            lines = q.strip().split("\n")
            if len(lines) < 6:
                continue

            question_text = lines[0].strip()
            options = [line[3:].strip() for line in lines[1:5]]
            correct_letter = lines[5].split(":")[-1].strip().lower()
            correct_index = {'a': 1, 'b': 2, 'c': 3, 'd': 4}.get(correct_letter)

            if question_text and correct_index:
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_text,
                    question_type="multiple-choice"
                )
                for idx, opt_text in enumerate(options, start=1):
                    Option.objects.create(
                        question=question,
                        text=opt_text,
                        is_correct=(idx == correct_index)
                    )
                created_count += 1

        return created_count

# --------------------------
# Quiz Admin with Ollama Form
# --------------------------

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    # ❌ Removed change_list_template to avoid template error

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "generate-ollama-questions/",
                self.admin_site.admin_view(self.generate_ollama_questions),
                name="generate_ollama_questions",
            ),
        ]
        return custom_urls + urls

    def generate_ollama_questions(self, request):
        if request.method == "POST":
            form = GenerateQuestionsForm(request.POST)
            if form.is_valid():
                quiz = form.cleaned_data["quiz"]
                prompt = form.cleaned_data["prompt"]
                num_questions = form.cleaned_data["num_questions"]
                difficulty = form.cleaned_data["difficulty"]

                try:
                    ai_response = generate_questions_with_ollama(prompt, num_questions, difficulty)
                except Exception as e:
                    messages.error(request, f"Ollama Error: {e}")
                    return redirect("..")

                created = 0
                for q in ai_response:
                    question_text = q.get("question")
                    options = q.get("options", [])
                    correct = q.get("answer", [])

                    if not question_text or len(options) < 2:
                        continue

                    question = Question.objects.create(
                        quiz=quiz,
                        text=question_text.strip(),
                        question_type="checkbox" if len(correct) > 1 else "radio",
                    )

                    for i, opt in enumerate(options):
                        question.options.create(text=opt.strip(), is_correct=(i in correct))

                    created += 1

                self.message_user(
                    request,
                    f"{created} questions generated and added to quiz: {quiz.title}",
                    messages.SUCCESS
                )
                return redirect("admin:quizzes_quiz_changelist")
        else:
            form = GenerateQuestionsForm()

        return TemplateResponse(request, "admin/quizzes/generate_ollama_questions.html", {"form": form})
