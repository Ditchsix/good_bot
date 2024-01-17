from googletrans import Translator


tr = Translator()


async def translator_text(text: str, lang: str):
    return tr.translate(text, dest=lang).text
    