from typing import Iterable

from aiogram import types
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .callback_data import (
    QuestionAnswerCallbackData,
    TicketCallbackData,
    TicketQuestionCallbackData,
)
from .phrases import phrases
from .utils.tickets import _TICKETS

remove_markup = types.ReplyKeyboardRemove(remove_keyboard=True)

tickets_markup = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(
                text=str(i + 1), callback_data=TicketCallbackData(ticket_idx=i).pack()
            )
            for i in range(len(_TICKETS))
        )
    )
    .as_markup()
)


def create_question_answers_markup(
    ticket_idx: int, question_idx: int, answers: Iterable[str]
):
    """Создать InlineKeyboardMarkup ответов на вопрос билета TicketQuestion

    Args:
        ticket_idx (int): индекс билета
        question_idx (int): индекс вопроса
        answers (Iterable[str]): ответы

    Returns:
        InlineKeyboardMarkup: клавиатура с ответами
    """

    return (
        InlineKeyboardBuilder()
        .add(
            *(
                InlineKeyboardButton(
                    text=str(i + 1),
                    callback_data=QuestionAnswerCallbackData(
                        ticket_idx=ticket_idx, question_idx=question_idx, answer_idx=i
                    ).pack(),
                )
                for i, answer in enumerate(answers)
            )
        )
        .adjust(3, repeat=True)
        .as_markup()
    )


def create_next_question_markup(ticket_idx: int, question_idx: int):
    """Создать клавиатуру перехода к следующему вопросу

    Args:
        ticket_idx (int): индекс билета
        question_idx (int): индекс вопроса

    Returns:
        InlineKeyboardMarkup: клавиатура с кнопкой для перехода к вопросу с индексом question_idx
    """

    return (
        InlineKeyboardBuilder()
        .button(
            text=phrases.next_question_button_text,
            callback_data=TicketQuestionCallbackData(
                ticket_idx=ticket_idx, question_idx=question_idx
            ),
        )
        .as_markup()
    )
