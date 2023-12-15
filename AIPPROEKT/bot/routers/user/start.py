from aiogram import types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from ... import markups
from ...callback_data import (
    QuestionAnswerCallbackData,
    TicketCallbackData,
    TicketQuestionCallbackData,
)
from ...core import bot
from ...phrases import phrases
from ...state.groups import TicketState
from ...utils import tickets
from . import router


def check_if_ticket_passed(state_data: TicketState.Data) -> bool:
    """Проверить пройден ли билет

    Args:
        state_data (TicketState.Data): данные состояния

    Returns:
        bool: True, если билет пройден, иначе False
    """

    return state_data["questions_len"] == state_data["right_answers_count"]


async def handle_next_question(
    question_message: types.Message,
    ticket_idx: int,
    question_idx: int,
    *,
    state: FSMContext,
    state_data: TicketState.Data
):
    """Функция конечного автомата для выдачи следующего вопроса билета

    Если следующего вопроса нет, то функция выдаст результат прохождения билета
    и закроет состояние

    Args:
        question_message (types.Message): сообщение билета
        ticket_idx (int): индекс билета
        question_idx (int): индекс следующего вопроса
        state (FSMContext): контекст состояния
        state_data (TicketState.Data): данные состояния

    Returns:
        None
    """

    ticket = tickets.get_ticket_by_idx(ticket_idx)

    try:
        question = ticket.questions[question_idx]
    except IndexError:
        await state.clear()
        await question_message.delete()

        if check_if_ticket_passed(state_data):
            return await bot.send_message(
                question_message.chat.id, phrases.passed_ticket_message_text
            )

        return await bot.send_message(
            question_message.chat.id,
            phrases.non_passed_ticket_message_text_fmt.format(**state_data),
        )

    media = types.InputMediaPhoto(
        media=types.FSInputFile(question.photo_path),
        caption=phrases.ticket_question_message_text_fmt.format(
            question=question,
            answers_fmt=phrases.format_question_answers(question.answers),
        ),
    )

    await question_message.edit_media(  # type: ignore
        media=media,
        reply_markup=markups.create_question_answers_markup(  # type: ignore
            ticket_idx, question_idx, question.answers
        ),
    )


@router.message(CommandStart())
async def start_command_handler(message: types.Message, state: FSMContext):
    """Хандлер команды /start (входной точки работы бота с пользователем)

    Args:
        message (types.Message): сообщение
        state (FSMContext): контекст состояния
    """

    await state.clear()
    await message.answer(
        phrases.start_message_text, reply_markup=markups.tickets_markup
    )


@router.callback_query(TicketCallbackData.filter())
async def ticket_handler(
    query: types.CallbackQuery, callback_data: TicketCallbackData, state: FSMContext
):
    """Хандлер выбора билета

    Args:
        query (types.CallbackQuery): CallbackQuery нажатия на кнопку
        callback_data (TicketCallbackData): CallbackData билета
        state (FSMContext): контекст состояния
    """

    ticket = tickets.get_ticket_by_idx(callback_data.ticket_idx)
    question = ticket.questions[0]

    await query.message.delete()  # type: ignore

    state_data: TicketState.Data = {
        "questions_len": len(ticket.questions),
        "right_answers_count": 0,
    }

    await state.set_state(TicketState.waiting_answer)
    await state.set_data(state_data)  # type: ignore

    await bot.send_photo(
        query.from_user.id,
        types.FSInputFile(question.photo_path),
        caption=phrases.ticket_question_message_text_fmt.format(
            question=question,
            answers_fmt=phrases.format_question_answers(question.answers),
        ),
        reply_markup=markups.create_question_answers_markup(
            callback_data.ticket_idx, 0, question.answers
        ),
    )


@router.callback_query(TicketState.waiting_answer, QuestionAnswerCallbackData.filter())
async def question_answer_handler(
    query: types.CallbackQuery,
    callback_data: QuestionAnswerCallbackData,
    state: FSMContext,
    state_data: TicketState.Data,
):
    """Хандлер выбора ответа

    Args:
        query (types.CallbackQuery): CallbackQuery кнопки выбора ответа
        callback_data (QuestionAnswerCallbackData): CallbackData ответа билета
        state (FSMContext): контекст состояния
        state_data (TicketState.Data): данные состояния
    """

    ticket = tickets.get_ticket_by_idx(callback_data.ticket_idx)
    question = ticket.questions[callback_data.question_idx]
    next_question_idx = callback_data.question_idx + 1

    if tickets.check_if_right_answer(question, callback_data.answer_idx):
        state_data["right_answers_count"] += 1

        await state.set_data(
            state_data,  # type: ignore
        )

        return await handle_next_question(
            query.message,  # type: ignore
            callback_data.ticket_idx,
            next_question_idx,
            state=state,
            state_data=state_data,
        )

    await query.message.edit_caption(  # type: ignore
        caption=phrases.invalid_answer_ticket_question_message_text_fmt.format(
            question=question, right_answer=question.answers[question.right_answer_idx]
        ),
        reply_markup=markups.create_next_question_markup(  # type: ignore
            callback_data.ticket_idx, next_question_idx
        ),
    )


@router.callback_query(TicketState.waiting_answer, TicketQuestionCallbackData.filter())
async def ticket_question_handler(
    query: types.CallbackQuery,
    callback_data: TicketQuestionCallbackData,
    state: FSMContext,
    state_data: TicketState.Data,
):
    """Хандлер перехода к следующему вопросу

    Args:
        query (types.CallbackQuery): CallbackQuery вопроса
        callback_data (TicketQuestionCallbackData): CallbackData вопроса
        state (FSMContext): контекст состояния
        state_data (TicketState.Data): данные состояния
    """

    await handle_next_question(
        query.message,  # type: ignore
        callback_data.ticket_idx,
        callback_data.question_idx,
        state=state,
        state_data=state_data,
    )
