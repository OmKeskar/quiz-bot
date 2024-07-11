
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if not answer:
        return False, "Answer cannot be empty."

    answers = session.get("answers", {})
    answers[current_question_id] = answer
    session["answers"] = answers

    return True, ""


def get_next_question(current_question_id):
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0

    current_index = current_question_id

    next_index = current_index + 1

    if next_index < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_index], next_index
    else:
        return "dummy question", -1


def generate_final_response(session):
    answers = session.get("answers", {})

    score = 0

    for idx, question in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question.get("correct_answer")
        user_answer = answers.get(idx)

        if user_answer == correct_answer:
            score += 1

    total_questions = len(PYTHON_QUESTION_LIST)

    result_message = f"Your score: {score} out of {total_questions}.\n"

    for idx, question in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question.get("correct_answer")
        user_answer = answers.get(idx)
        question_text = question.get("question")

        result_message += f"\nQuestion {idx + 1}: {question_text}\n"
        result_message += f"Your answer: {user_answer}\n"
        result_message += f"Correct answer: {correct_answer}\n"

    return result_message
