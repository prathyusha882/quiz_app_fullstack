from django import forms
from .models import Quiz

class GenerateQuestionsForm(forms.Form):
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        required=True,
        label="Select Quiz"
    )
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        label="AI Prompt",
        help_text="Describe the type of questions you want the AI to generate. For example: 'Generate 5 easy multiple-choice questions on Python basics.'",
        initial="Generate 5 multiple-choice questions on Python basics."
    )
    num_questions = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=5,
        label="Number of Questions"
    )
    difficulty = forms.ChoiceField(
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        initial="medium",
        label="Difficulty"
    )

