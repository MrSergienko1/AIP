from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class BotPhrases:
    """Класс с шаблонами ответов бота"""

    bot_started = "Бот {me.username} успешно запущен"
    start_message_text = "Выберите билет для решения"
    ticket_question_message_text_fmt = """{question.question_text}
    
{answers_fmt}"""
    invalid_answer_ticket_question_message_text_fmt = """{question.question_text}
    
Правильный ответ:
{right_answer}

Комментарий:
{question.comment}"""
    next_question_button_text = "Следующий вопрос"
    passed_ticket_message_text = "Билет сдан"
    non_passed_ticket_message_text_fmt = """Билет не сдан
    
Всего вопросов: {questions_len}
Правильных ответов: {right_answers_count}"""

    def format_question_answers(self, answers: Iterable[str]) -> str:
        return f"\n".join(f"{i + 1}. {answer}" for i, answer in enumerate(answers))


phrases = BotPhrases()
