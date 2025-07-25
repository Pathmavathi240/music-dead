from pyrogram import filters
from DeadlineTech import app
from pyrogram import filters

@app.on_message(filters.command("biolink") & filters.group)
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from config import OWNER_ID
import re

BIO_PROTECT_ENABLED = {}
USER_WARNINGS = {}

# Toggle bio protection
@Client.on_message(filters.command("biolink") & filters.group)
async def biolink_toggle(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ இந்த கட்டளை மட்டுமே OWNER மட்டுமே பயன்படுத்த முடியும்.")

    if len(message.command) < 2:
        return await message.reply_text("✅ Usage: `/biolink on` அல்லது `/biolink off`")

    cmd = message.command[1].lower()
    chat_id = message.chat.id

    if cmd == "on":
        BIO_PROTECT_ENABLED[chat_id] = True
        await message.reply_text("✅ Bio link பாதுகாப்பு **ஓன்** செய்யப்பட்டது.")
    elif cmd == "off":
        BIO_PROTECT_ENABLED[chat_id] = False
        await message.reply_text("❌ Bio link பாதுகாப்பு **ஆஃப்** செய்யப்பட்டது.")
    else:
        await message.reply_text("ℹ️ பயன்பாடு: `/biolink on` அல்லது `/biolink off`")

# Main bio link checker
@Client.on_message(filters.text & filters.group)
async def check_bio_links(client, message: Message):
    chat_id = message.chat.id
    user = message.from_user

    if not user or user.is_bot:
        return

    if not BIO_PROTECT_ENABLED.get(chat_id, False):
        return

    if user.id == OWNER_ID:
        return

    try:
        member = await client.get_chat_member(chat_id, user.id)
        if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return
    except:
        return

    try:
        bio = (await client.get_users(user.id)).bio or ""
    except:
        return

    if re.search(r"(https?://|t\.me/|www\.)", bio):
        key = f"{chat_id}:{user.id}"
        warn_count = USER_WARNINGS.get(key, 0)

        if warn_count == 0:
            USER_WARNINGS[key] = 1
            await message.reply_text(
                f"🚨 {user.mention} உங்கள் Bio-வில் link உள்ளது!\n"
                f"⚠️ இது **முதல்** warning. மீண்டும் link இருந்தால் **தானாக ban** செய்யப்படும்!"
            )
        else:
            try:
                await client.ban_chat_member(chat_id, user.id)
                USER_WARNINGS.pop(key, None)
                await message.reply_text(
                    f"🚫 {user.mention} Bio-வில் மீண்டும் link கண்டறியப்பட்டது.\n"
                    f"🔨 **User has been banned automatically!**"
                )
            except Exception as e:
                await message.reply_text(f"❌ Ban செய்ய முடியவில்லை: {e}")

# Check warn count manually
@Client.on_message(filters.command("warns") & filters.group)
async def check_warn_count(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ இந்த கட்டளை Owner மட்டுமே பயன்படுத்த முடியும்.")

    if len(message.command) < 2:
        return await message.reply_text("ℹ️ Usage: `/warns <user_id>`")

    try:
        user_id = int(message.command[1])
        chat_id = message.chat.id
        key = f"{chat_id}:{user_id}"
        count = USER_WARNINGS.get(key, 0)
        await message.reply_text(f"🔎 User `{user_id}` has {count}/1 warning.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
