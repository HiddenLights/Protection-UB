from pyrogram import Client
from sample_config import *
from pyrogram.errors import UserAlreadyParticipant
from Python_ARQ import ARQ
from aiohttp import ClientSession
from pyrogram.types import Message
from inspect import getfullargspec

app = Client(
        SESSION_STRING,
        API_ID,
        API_HASH 
        )
aiohttpsession = ClientSession()        
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

USERBOT_PREFIX = USERBOT_PREFIX

async def main():
        try:
            await app.join_chat("szteambots")
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            print(e)
            pass
app.run(main())
app.start()

async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
