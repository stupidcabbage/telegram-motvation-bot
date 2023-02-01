import aiogram.utils.markdown as fmt
from app.servises.get_images import get_image


async def make_start_text(first_name: str) -> str:
    image = await get_image()
    text = (fmt.hbold(f"Привет, {first_name}! 🧟‍♂️\n\n") +
            "Тебе совсем не хватает мотивации?\n" +
            "Пропиши /quote, услышь великих людей!\n\n" +
            "Хочешь получать их чаще?\n" +
            "Пропиши /set_time и получай их когда тебе будет удобно!" +
            f"{fmt.hide_link(image)}")
    return text


HELP_TEXT = ("<b>Воспользуйся командой, приведенной в списке ниже👇</b>\n\n" +
        "📌 Добавить время в расписание отправок -> /set_time\n\n" +
        "📪 Удалить время из расписания -> /delete_time\n\n" +
        "🗓 Узнать свое расписание -> /schedule\n\n" +
        "🔖 Получить новую цитату -> /quote")
