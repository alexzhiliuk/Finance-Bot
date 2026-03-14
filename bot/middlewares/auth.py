import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.config import ALLOWED_USER_IDS

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    """Silently drops updates from users not in ALLOWED_USER_IDS.
    If ALLOWED_USER_IDS is empty, all users are allowed (dev mode)."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not ALLOWED_USER_IDS:
            logger.warning("ALLOWED_USER_IDS не задан — бот доступен всем пользователям")
            return await handler(event, data)

        user = data.get("event_from_user")
        if user is None or user.id not in ALLOWED_USER_IDS:
            if user:
                logger.info("Отклонён запрос от неавторизованного пользователя: %s (@%s)", user.id, user.username)
            return  # молча игнорируем

        return await handler(event, data)
