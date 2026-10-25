import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def transcribe_and_parse(audio: bytes, filename: str):
    tmp = f"/tmp/{filename}"
    with open(tmp, "wb") as f:
        f.write(audio)

    with open(tmp, "rb") as f:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)

    text = transcript.text
    items = []
    for token in text.replace(",", " ").split():
        if any(ch.isdigit() for ch in token):
            items.append({"product_query": token, "quantity": 1})
    return text, items