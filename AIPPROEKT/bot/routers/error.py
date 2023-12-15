import logging

from aiogram import Router

from . import root_router

router = Router()
root_router.include_router(router)


@router.errors()
async def errors_handler(error: Exception):
    """Хандлер для отлавливания ошибок

    Args:
        error (Exception): ошибка, упавшая в другом хандлере
    """

    logging.error(error, exc_info=True)
