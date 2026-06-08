import asyncio
from audio import stt
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os

os.environ["OPENROUTER_API_KEY"] = "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"

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)
async_client = AsyncOpenAI()

SYSTEM_PROMPT = f""" 
    you are an expert voice agent.You are given the transcript of what
    user said and you have to respond to the user in a helpful way.
    you need to output as if you are a voice agent and whatever
    you speak will be converted back to audio using AI and played back to user.

"""

async def tts(speech:str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="always speak in cheerfull manner with full of delight and happiness",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)
def main():
    user_query=stt()
    response=client.chat.completions.create(
        model="openrouter/owl-alpha",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    print("==========AI Response==========\n")
    print(response.choices[0].message.content)
    asyncio.run(tts(speech=response.choices[0].message.content))

main()