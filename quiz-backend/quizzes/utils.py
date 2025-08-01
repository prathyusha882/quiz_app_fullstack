import re
from .models import Question, Option

def save_questions_from_text(text, quiz):
    question_blocks = re.split(r'\n(?=Q\d+:)', text.strip())
    created_count = 0

    for block in question_blocks:
        q_match = re.search(r'Q\d+:\s*(.+?)\n', block)
        if not q_match:
            continue
        question_text = q_match.group(1).strip()

        options = re.findall(r'([A-D])\.\s*(.+)', block)
        correct_match = re.search(r'Answer:\s*([A-D](?:,[A-D])*)', block)

        if not options or not correct_match:
            continue

        question = Question.objects.create(
            quiz=quiz,
            text=question_text,
            question_type='checkbox' if ',' in correct_match.group(1) else 'radio'
        )

        correct_answers = [ans.strip() for ans in correct_match.group(1).split(',')]
        for label, option_text in options:
            Option.objects.create(
                question=question,
                text=option_text.strip(),
                is_correct=label in correct_answers
            )
        created_count += 1

    return created_count
