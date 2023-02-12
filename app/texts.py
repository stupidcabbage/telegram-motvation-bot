import aiogram.utils.markdown as fmt
from app.services.get_images import get_image


async def make_start_text(first_name: str) -> str:
    image = await get_image()
    text = (fmt.hbold(f"Привет, {first_name}! 🧟‍♂️\n\n") +
            "Тебе совсем не хватает мотивации?\n" +
            "Пропиши /quote, услышь великих людей!\n\n" +
            "Хочешь получать их чаще?\n" +
            "Пропиши /set_time и получай их когда тебе будет удобно!" +
            f"{fmt.hide_link(image)}")
    return text


HELP = ("<b>Воспользуйся командой, приведенно   й в списке ниже👇</b>\n\n" +
        "📌 Добавить время в расписание отправок -> /set_time\n\n" +
        "📪 Удалить время из расписания -> /delete_time\n\n" +
        "🗓 Узнать свое расписание -> /schedule\n\n" +
        "🔖 Получить новую цитату -> /quote")

SET_TIME = "<b>📍 Отправьте время, в которое Вам присылать цитату.</b> "

HAS_SETTED_TIME = ('<b>📬 Это время уже есть в расписании!</b>\n\n' +
                   '🗓 Посмотреть свое расписание - /schedule')

ERROR_SET_TIME = ('<b>❗️ Проверьте корректность написания времени!</b>\n\n' +
                        'Пример правильного написания: 11:00, 1:01, 15-12')

ERROR_DELETE_TIME = (ERROR_SET_TIME +
                     "\n\n🤸‍♂️Чтобы полностью очистить расписание напишите: все")

DELETE_QUESTION = '<b>✂️ Какое время удалить из расписания?</b>'
