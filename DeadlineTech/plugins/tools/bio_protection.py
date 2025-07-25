from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from DeadlineTech import app
from config import OWNER_ID
import re

BIO_PROTECT_ENABLED = {}
USER_WARNINGS = {}
BOT_ADDED_BY = {}

# Track who added the bot
@app.on_message(filters.new_chat_members)
async def handle_new_members(client, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        if member.id == (await app.get_me()).id:
            BOT_ADDED_BY[chat_id] = message.from_user.id
        else:
            # Check bio protection on
            if not BIO_PROTECT_ENABLED.get(chat_id, False):
                return
            if member.id == OWNER_ID:
                return

            try:
                chat_member = await client.get_chat_member(chat_id, member.id)
                if chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                    return
            except:
                return

            try:
                user_info = await client.get_users(member.id)
                bio = user_info.bio or ""
            except:
                return

            # Check for links
            if re.search(r"(https?://|t\.me/|telegram\.me/|www\.)", bio, re.IGNORECASE):
                key = f"{chat_id}:{member.id}"
                warn_count = USER_WARNINGS.get(key, 0)

                if warn_count == 0:
                    USER_WARNINGS[key] = 1
                    await message.reply_text(
                        f"🚨 {member.mention} உங்கள் Bio-வில் link உள்ளது!\n"
                        f"⚠️ இது **முதல்** warning. மீண்டும் Bio-வில் link இருந்தால் **தானாக ban** செய்யப்படும்!"
                    )
                else:
                    try:
                        await client.ban_chat_member(chat_id, member.id)
                        USER_WARNINGS.pop(key, None)
                        await message.reply_text(
                            f"🚫 {member.mention} Bio-வில் மீண்டும் link கண்டறியப்பட்டது.\n"
                            f"🔨 **User has been banned automatically!**"
                        )
                    except Exception as e:
                        await message.reply_text(f"❌ Ban செய்ய முடியவில்லை: {e}")

# Toggle command for /biolink on/off
@app.on_message(filters.command("biolink") & filters.group)
async def biolink_toggle(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Permission check
    if user_id == OWNER_ID:
        is_allowed = True
    else:
        try:
            member = await client.get_chat_member(chat_id, user_id)
            is_allowed = (
                member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
                or BOT_ADDED_BY.get(chat_id) == user_id
            )
        except:
            is_allowed = False

    if not is_allowed:
        return await message.reply_text("❌ இந்த கட்டளை Owner, Admin, அல்லது Bot-ஐ சேர்த்தவர் மட்டுமே பயன்படுத்தலாம்.")

    if len(message.command) < 2:
        return await message.reply_text("ℹ️ பயன்பாடு: `/biolink on` அல்லது `/biolink off`")

    cmd = message.command[1].lower()
    if cmd == "on":
        BIO_PROTECT_ENABLED[chat_id] = True
        await message.reply_text("✅ Bio link பாதுகாப்பு **ஓன்** செய்யப்பட்டது.")
    elif cmd == "off":
        BIO_PROTECT_ENABLED[chat_id] = False
        await message.reply_text("❌ Bio link பாதுகாப்பு **ஆஃப்** செய்யப்பட்டது.")
    else:
        await message.reply_text("ℹ️ `/biolink on` அல்லது `/biolink off` பயன்படுத்தவும்.")

# Check current warnings
@app.on_message(filters.command("warns") & filters.group)
async def check_warn_count(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ இந்த கட்டளை Owner மட்டுமே பயன்படுத்த முடியும்.")

    if len(message.command) < 2:
        return await message.reply_text("ℹ️ பயன்பாடு: `/warns <user_id>`")

    try:
        user_id = int(message.command[1])
        chat_id = message.chat.id
        key = f"{chat_id}:{user_id}"
        count = USER_WARNINGS.get(key, 0)
        await message.reply_text(f"🔎 User `{user_id}` has {count}/1 warning.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
