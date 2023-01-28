from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot) -> None:
    """Устанавливает команды, отображаемые при вводе."""
    commands = [
        BotCommand(command="/start", description="Начальная команда"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/quote", description="Получить новое высказывание"),
        BotCommand(command="/schedule", description="Посмотреть расписание отправок"),
        BotCommand(command="/set_time", description="Установить время отправки цитаты"),
        BotCommand(command='/delete_time', description='Удалить время из расписания')
    ]
    await bot.set_my_commands(commands)
