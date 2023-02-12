import aiohttp


async def get_image():
    """Возвращает словарь с автором и текстом цитаты на русском языке,
    полученные с api.forismatic.com/api/1.0/"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'https://api.thecatapi.com/v1/images/search') as resp:
            json_result = await resp.json()
            return json_result[0].get('url')
