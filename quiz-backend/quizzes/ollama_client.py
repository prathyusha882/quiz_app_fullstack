# quizzes/ollama_client.py
import requests
import json

def generate_questions_with_ollama(prompt, num_questions=5, difficulty="medium"):
    try:
        ollama_prompt = f"""
Generate {num_questions} {difficulty} level multiple-choice quiz questions on the following topic:

{prompt}

Return JSON in the following format:

[
  {{
    "question": "Your question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": [0]  // Indices of correct options (e.g., [0] for single-answer, [1, 2] for checkbox)
  }},
  ...
]
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": ollama_prompt,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json().get("response", "")

        # Extract JSON from raw response
        start = data.find("[")
        end = data.rfind("]") + 1
        questions_json = data[start:end]
        parsed = json.loads(questions_json)

        cleaned = []
        for item in parsed:
            question = item.get("question")
            options = item.get("options", [])
            answer = item.get("answer", [])

            if question and options and isinstance(answer, list):
                cleaned.append({
                    "question": question,
                    "options": options,
                    "answer": answer,
                })
        return cleaned

    except Exception as e:
        print("Error generating questions:", e)
        return []
