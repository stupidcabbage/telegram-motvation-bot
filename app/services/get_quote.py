import aiohttp

PARAMS = {
    'method': 'getQuote',
    'lang': 'ru',
    'format': 'json'
}


async def get_quote() -> dict[str, str]:
    """Возвращает словарь с автором и текстом цитаты на русском языке,
    полученные с api.forismatic.com/api/1.0/"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'http://api.forismatic.com/api/1.0/',
                params=PARAMS) as resp:
            json_result = await resp.json()
            return {'author': json_result.get('quoteAuthor'),
                    'text': json_result.get('quoteText')}


async def get_reserve_quote() -> dict[str, str]:
    """Возвращает словарь с автором и текстом цитаты на английском языке,
    полученные с favqs.com/api/qotd"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'https://favqs.com/api/qotd') as resp:
            json_result = (await resp.json()).get('quote')
            return {'author': json_result.get('author'),
                    'text': json_result.get('body')}
