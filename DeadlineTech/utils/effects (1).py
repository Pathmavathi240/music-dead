
import asyncio

# Effect 1: Typing Welcome Text Slowly
async def effect_typing(message, welcome_text):
    typing = await message.reply_text("")
    for char in welcome_text:
        await typing.edit_text(typing.text + char)
        await asyncio.sleep(0.07)
    await asyncio.sleep(1.2)
    return typing

# Effect 2: Spinner Emoji Animation
async def effect_spinner(message):
    spinner_emojis = ["🌀", "✨", "💫", "⚡", "🎵", "🎶"]
    for emoji in spinner_emojis:
        spin = await message.reply_text(emoji)
        await asyncio.sleep(0.3)
        await spin.delete()

# Effect 3: Dot Loading Bar
async def effect_dots(message):
    loading = await message.reply_text("Loading")
    for i in range(1, 5):
        await loading.edit_text("Loading" + "." * i)
        await asyncio.sleep(0.5)
    await asyncio.sleep(1.2)
    return loading

# Effect 4: Emoji Progress Bar
async def effect_progressbar(message):
    bar = ["[░░░░░]", "[█░░░░]", "[██░░░]", "[███░░]", "[████░]", "[█████]"]
    progress = await message.reply_text(bar[0])
    for b in bar[1:]:
        await asyncio.sleep(0.4)
        await progress.edit_text(b)
    await asyncio.sleep(1)
    return progress

# Effect 5: Ding Dong Text Animation
async def effect_dingdong(message):
    ding_texts = ["🔔", "🔔 Ding", "🔔 Ding Dong", "🔔 Ding Dong Start..."]
    ding = await message.reply_text(ding_texts[0])
    for text in ding_texts[1:]:
        await asyncio.sleep(0.5)
        await ding.edit_text(text)
    await asyncio.sleep(1)
    return ding

# Effect 6: Flash Emojis
async def effect_flash(message):
    flash_emojis = ["⚡", "✨", "🔥", "💥", "🌟", "🚀"]
    flash = await message.reply_text("")
    for emoji in flash_emojis:
        await flash.edit_text(emoji)
        await asyncio.sleep(0.2)
    await asyncio.sleep(1)
    return flash
