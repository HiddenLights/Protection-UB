from os import remove
from pyrogram import filters
from pyrogram import filters
from pyrogram.types import Message
from rose import eor, app, arq, USERBOT_PREFIX


ns_active_chats = []
as_active_chats = []
ans_active_chats = []


async def ans_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "Enabled AntiService System. I will Delete Service Messages from Now on."
            return await eor(message, text=text)
        await eor(message, text="system Is Already Enabled.")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text="❌ Disabled System.")
        await eor(message, text="Disabled AntiService System. I won't Be Deleting Service Message from Now on.")
    else:
        await eor(message, text=f"**Usage:** {USERBOT_PREFIX}antinsfw `[on/off]`")


# Enabled | Disable NSFW
@app.on_message(
    filters.command("antiservice", prefixes=USERBOT_PREFIX)
)
async def ans_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text=f"**Usage:** {USERBOT_PREFIX}antiservice `[on/off]`")
    await ans_toggle(ans_active_chats, message)

async def nsfw_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "✅ Enabled **AntiNSFW** System. I will Delete Messages Containing Inappropriate Content."
            return await eor(message, text=text)
        await eor(message, text="**AntiNSFW** System Is Already Enabled.")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text="❌ Disabled AntiNSFW System.")
        await eor(message, text="**AntiNSFW** System Already Disabled.")
    else:
        await eor(message, text=f"**Usage:** {USERBOT_PREFIX}antinsfw `[on/off]`")


# Enabled | Disable NSFW
@app.on_message(
    filters.command("antinsfw", prefixes=USERBOT_PREFIX)
)
async def nsfw_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text=f"**Usage:** {USERBOT_PREFIX}antinsfw `[on/off]`")
    await nsfw_toggle(ns_active_chats, message)


async def spam_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "✅ Enabled **Anti-SPAM** System. I will Delete spam Messages."
            return await eor(message, text=text)
        await eor(message, text="**Anti-SPAM** System Is Already Enabled.")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text="❌ Disabled Anti-SPAM System.")
        await eor(message, text="**Anti-SPAM** System Already Disabled.")
    else:
        await eor(message, text=f"**Usage:** {USERBOT_PREFIX}antispam `[on/off]`")


# Enabled | Disable SPAM
@app.on_message(
    filters.command("antispam", prefixes=USERBOT_PREFIX)
)
async def spam_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text=f"**Usage:** {USERBOT_PREFIX}antispam `[on/off]`")
    await spam_toggle(ns_active_chats, message)


#nsfw detect
@app.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=8,
)
async def detect_nsfw(_, message):
    if message.chat.id not in ns_active_chats:
        return
    if not message.from_user:
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await app.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    if not results.ok:
        return
    results = results.result
    remove(file)
    nsfw = results.is_nsfw
    if not nsfw:
        return
    try:
        await message.delete()
    except Exception:
        return
    await message.reply_text(
        f"""
**Pron Detected & Deleted Successfully!
————————————————————**
★ **User:** {message.from_user.mention} [`{message.from_user.id}`]
★ **Neutral:** `{results.neutral} %`
★ **Porn:** `{results.porn} %`
★ **Adult:** `{results.sexy} %`
★ **Hentai:** `{results.hentai} %`
★ **Drawings:** `{results.drawings} %`
**————————————————————**
__Powered By @szteambots__
"""
    )


# get file method
async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


#spam detect
@app.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=30,
)
async def detect_spam(_, message):
    if message.chat.id not in as_active_chats:
        return
    if not message.from_user:
        return
    text = message.text or message.caption
    if not text:
        return
    resp = await arq.nlp(text)
    if not resp.ok:
        return
    result = resp.result[0]
    if not result.is_spam:
        return
    try:
        await message.delete()
    except Exception:
        return
    await message.reply_text(
        f"""
**Spam Detected & Deleted Successfully!
★ **User:** {message.from_user.mention} [`{message.from_user.id}`]
__Powered By @szteambots__
"""
    )       


#spamscan 
@app.on_message(
    filters.command("spamscan", prefixes=USERBOT_PREFIX)
)
async def scanNLP(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to scan it.")
    r = message.reply_to_message
    text = r.text or r.caption
    if not text:
        return await message.reply("Can't scan that")
    data = await arq.nlp(text)
    data = data.result[0]
    msg = f"""
**Is Spam:** {data.is_spam}
**Spam Probability:** {data.spam_probability} %
**Spam:** {data.spam}
**Ham:** {data.ham}
**Profanity:** {data.profanity}
"""
    await message.reply(msg, quote=True)

#nsfwscan 
@app.on_message(
    filters.command("nsfwscan", prefixes=USERBOT_PREFIX)
)
async def nsfw_scan_command(_, message):
    if not message.reply_to_message:
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    m = await message.reply_text("Scanning")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("Something wrong happened.")
    file = await app.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
★ **Neutral:** `{results.neutral} %`
★ **Porn:** `{results.porn} %`
★ **Hentai:** `{results.hentai} %`
★ **Sexy:** `{results.sexy} %`
★ **Drawings:** `{results.drawings} %`
★ **NSFW:** `{results.is_nsfw}`
"""
    )

@app.on_message(filters.service, group=11)
async def delete_service(_, message):
    try:
        if message.chat.id not in ans_active_chats:
            return await message.delete()
    except Exception as e:
        pass
        await message.reply(f"{e}")  


@app.on_message(
    filters.command("help", prefixes=USERBOT_PREFIX)
)
async def help(_, message: Message):
    await message.reply(f"""
--**Commands**--:

• `{USERBOT_PREFIX}help` - shows help for all commands
• `{USERBOT_PREFIX}antispam`[on/off] - automatically delete messages that contains spam or promoting links
• `{USERBOT_PREFIX}antinsfw`[on/off] - automatically delete messages that contains pornographic content
• `{USERBOT_PREFIX}spamscan`[reply message] - Ditect contains spam or promoting links
• `{USERBOT_PREFIX}nsfwscan`[reply media] - Ditect contains pornographic content
• `{USERBOT_PREFIX}antiservice`[on/off] - Remove Service Message In Groups Like Users Join Messages, Leave Messages, 
Pinned Allert Messages, Voice Chat Invite Members Allerts ETC...

© **Powered By**
@szteambots | @slbotzone 
    """)
    