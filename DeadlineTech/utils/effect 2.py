import asyncio
from pyrogram.types import Message

# Main Effect Handler
effects_list = {}

# Effect 1: Typing One by One
async def effect_typing(client, message: Message, welcome_text: str):
    typing = await message.reply_text("")
    for char in welcome_text:
        await typing.edit_text(typing.text + char)
        await asyncio.sleep(0.08)
    await asyncio.sleep(1.2)
    await typing.delete()

# Effect 2: Spinner Emojis
async def effect_spinner(client, message: Message):
    emojis = ["🌀", "✨", "💫", "⚡", "🎵", "🎶"]
    for emoji in emojis:
        spin = await message.reply_text(emoji)
        await asyncio.sleep(0.25)
        await spin.delete()

# Effect 3: Flash Emoji Typing
async def effect_flash_typing(client, message: Message, welcome_text: str):
    emojis = ["🔆", "✨", "💡"]
    for emoji in emojis:
        flash = await message.reply_text(f"{emoji} {welcome_text}")
        await asyncio.sleep(0.4)
        await flash.delete()

# Effect 4: Typing then Emoji Rain
async def effect_emoji_rain(client, message: Message, welcome_text: str):
    msg = await message.reply_text("")
    for char in welcome_text:
        await msg.edit_text(msg.text + char)
        await asyncio.sleep(0.05)
    await asyncio.sleep(0.6)
    rain = await message.reply_text("☔🎶✨🎵💧")
    await asyncio.sleep(1.2)
    await rain.delete()

# Effect 5: Rainbow Effect (colored characters using Markdown)
async def effect_rainbow(client, message: Message, welcome_text: str):
    colors = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
    rainbow = ""
    for i, char in enumerate(welcome_text):
        rainbow += f"{colors[i % len(colors)]}{char}"
        await asyncio.sleep(0.05)
    await message.reply_text(rainbow)

# Effect 6: Backspace Effect
async def effect_backspace(client, message: Message, welcome_text: str):
    msg = await message.reply_text("")
    for char in welcome_text:
        await msg.edit_text(msg.text + char)
        await asyncio.sleep(0.06)
    await asyncio.sleep(0.5)
    for _ in welcome_text:
        await msg.edit_text(msg.text[:-1])
        await asyncio.sleep(0.04)
    await asyncio.sleep(0.3)
    await msg.edit_text(welcome_text)
    await asyncio.sleep(1.2)
    await msg.delete()

# Effect 7: Dot Wave Effect
async def effect_dot_wave(client, message: Message):
    dots = [".  ", ". .  ", ". . .", " . .", "  ."]
    for frame in dots:
        dot = await message.reply_text(frame)
        await asyncio.sleep(0.25)
        await dot.delete()

# Effect 8: Emoji Scroll
async def effect_scroll_emoji(client, message: Message):
    emojis = ["🎧", "🎶", "🎼", "🎹", "🎷", "🥁", "🎺"]
    text = ""
    scroll = await message.reply_text("")
    for emoji in emojis:
        text += emoji
        await scroll.edit_text(text)
        await asyncio.sleep(0.2)
    await asyncio.sleep(1)
    await scroll.delete()

# Effect 9: Typing with Color Dot at End
async def effect_typing_dot(client, message: Message, welcome_text: str):
    dots = ["🔴", "🟠", "🟢", "🔵", "🟣"]
    typing = await message.reply_text("")
    for char in welcome_text:
        await typing.edit_text(typing.text + char)
        await asyncio.sleep(0.07)
    for dot in dots:
        await typing.edit_text(typing.text + " " + dot)
        await asyncio.sleep(0.25)
    await asyncio.sleep(1)
    await typing.delete()

# Register effects
effects_list = {
    1: effect_typing,
    2: effect_spinner,
    3: effect_flash_typing,
    4: effect_emoji_rain,
    5: effect_rainbow,
    6: effect_backspace,
    7: effect_dot_wave,
    8: effect_scroll_emoji,
    9: effect_typing_dot,
}

def get_effect(effect_id):
    return effects_list.get(effect_id, effect_typing)
  
