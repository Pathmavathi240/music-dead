from pyrogram import filters
from pyrogram.types import Message, ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from DeadlineTech import app
from config import OWNER_ID
import re

# Bio protection state per group
BIO_PROTECT_ENABLED = {}

# User warnings
USER_WARNINGS = {}

# Track who added the bot
BOT_ADDED_BY = {}

# Toggle bio protection ON/OFF (OWNER ONLY)
@app.on_message(filters.command("biolink") & filters.group)
async def biolink_toggle(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        return await message.reply_text("❌ இந்த கட்டளை Owner மட்டுமே பயன்படுத்த முடியும்.")

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

# Track who added the bot
@app.on_message(filters.new_chat_members)
async def track_bot_adder(client, message: Message):
    for member in message.new_chat_members:
        if member.id == (await app.get_me()).id:
            BOT_ADDED_BY[message.chat.id] = message.from_user.id

# Detect bio link when user joins
@app.on_chat_member_updated()
async def bio_link_checker(client, chat_member: ChatMemberUpdated):
    chat_id = chat_member.chat.id
    user = chat_member.new_chat_member.user
    status = chat_member.new_chat_member.status

    if status != ChatMemberStatus.MEMBER:
        return

    if not BIO_PROTECT_ENABLED.get(chat_id, False):
        return

    if user.is_bot or user.id == OWNER_ID:
        return

    try:
        member = await client.get_chat_member(chat_id, user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
    except:
        return

    try:
        user_info = await client.get_users(user.id)
        bio = user_info.bio or ""
    except:
        return

    # Check for links in bio
    if re.search(r"(https?://|t\.me/|telegram\.me/|instagram|youtube|onlyfans|porn|www\.)", bio, re.IGNORECASE):
        key = f"{chat_id}:{user.id}"
        warn_count = USER_WARNINGS.get(key, 0)

        if warn_count == 0:
            USER_WARNINGS[key] = 1
            await client.send_message(
                chat_id,
                f"🚨 {user.mention} உங்கள் Bio-வில் link உள்ளது!\n"
                f"⚠️ இது **முதல்** warning. மீண்டும் Bio-வில் link இருந்தால் **தானாக ban** செய்யப்படும்!"
            )
        else:
            try:
                await client.ban_chat_member(chat_id, user.id)
                USER_WARNINGS.pop(key, None)
                await client.send_message(
                    chat_id,
                    f"🚫 {user.mention} Bio-வில் மீண்டும் link கண்டறியப்பட்டது.\n"
                    f"🔨 **User has been banned automatically!**"
                )
            except Exception as e:
                await client.send_message(chat_id, f"❌ Ban செய்ய முடியவில்லை: {e}")

# Check warning count
@app.on_message(filters.command("warns") & filters.group)
async def check_warns(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ இந்த கட்டளை Owner மட்டுமே பயன்படுத்த முடியும்.")
    
    if len(message.command) < 2:
        return await message.reply_text("ℹ️ பயன்பாடு: `/warns <user_id>`")

    try:
        user_id = int(message.command[1])
        key = f"{message.chat.id}:{user_id}"
        count = USER_WARNINGS.get(key, 0)
        await message.reply_text(f"🔎 User `{user_id}` has {count}/1 warning.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
