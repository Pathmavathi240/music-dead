from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from DeadlineTech import app
from config import OWNER_ID
import re

# Bio protection state per group
BIO_PROTECT_ENABLED = {}

# User warnings
USER_WARNINGS = {}

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

# Detect bio link when new user joins
@app.on_message(filters.new_chat_members)
async def new_member_bio_check(client, message: Message):
    chat_id = message.chat.id

    if not BIO_PROTECT_ENABLED.get(chat_id, False):
        return

    for user in message.new_chat_members:
        if user.is_bot or user.id == OWNER_ID:
            continue

        try:
            # Skip if user is admin
            member = await client.get_chat_member(chat_id, user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                continue
        except:
            continue

        try:
            user_info = await client.get_users(user.id)
            bio = user_info.bio or ""
        except:
            continue

        # Debug print (optional)
        print(f"👤 {user.first_name}'s bio: {bio}")

        # Check for links in bio
        if re.search(r"(https?://|t\.me|telegram\.me|instagram|youtube|onlyfans|porn|www\.)", bio, re.IGNORECASE):
            key = f"{chat_id}:{user.id}"
            warn_count = USER_WARNINGS.get(key, 0)

            if warn_count == 0:
                USER_WARNINGS[key] = 1
                await message.reply_text(
                    f"🚨 {user.mention} உங்கள் Bio-வில் link உள்ளது!\n"
                    f"⚠️ இது **முதல்** warning. மீண்டும் Bio-வில் link இருந்தால் **தானாக ban** செய்யப்படும்!"
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
