import json
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def _craft_prompt(topic, difficulty, num_questions=1):
    return f"""
    Generate {num_questions} multiple-choice quiz questions about {topic} at {difficulty} difficulty.
    Each question should have:
    - "question": the question text
    - "options": a list of 4 strings
    - "correct_answer": the correct option string
    - "type": "multiple-choice"

    Format the output as a JSON array.
    """

def generate_questions_from_ai(topic, difficulty, num_questions=5):
    prompt = _craft_prompt(topic, difficulty, num_questions)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates quiz questions."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response.choices[0].message["content"]

    # Clean and parse response
    if raw_text.startswith("```json"):
        raw_text = raw_text.strip("```json").strip("```").strip()

    questions_data = json.loads(raw_text)

    # Validate
    validated = []
    for q in questions_data:
        if all(k in q for k in ["question", "options", "correct_answer", "type"]):
            validated.append({
                "text": q["question"],
                "question_type": q["type"],
                "options": [
                    {"text": opt, "is_correct": opt == q["correct_answer"]}
                    for opt in q["options"]
                ]
            })

    return validated
