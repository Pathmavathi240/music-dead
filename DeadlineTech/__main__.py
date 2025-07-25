# Powered By Team DeadlineTech

import asyncio
import importlib

from pyrogram.types import BotCommand
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from DeadlineTech import LOGGER, app, userbot
from DeadlineTech.core.call import Anony
from DeadlineTech.misc import sudo
from DeadlineTech.plugins import ALL_MODULES
from DeadlineTech.utils.database import get_banned_users, get_gbanned
from DeadlineTech.utils.crash_reporter import setup_global_exception_handler
from config import BANNED_USERS

async def init():
    # ✅ Enable global crash handler
    setup_global_exception_handler()

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()

    await app.set_bot_commands([
        BotCommand("start", "Sᴛᴀʀᴛ's Tʜᴇ Bᴏᴛ"),
        BotCommand("clone", "Start your own bot now"),
        BotCommand("ping", "Cʜᴇᴄᴋ ɪғ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ"),
        BotCommand("help", "Gᴇᴛ Cᴏᴍᴍᴀɴᴅs Lɪsᴛ"),
        BotCommand("music", "Download the songs 🎵"),
        BotCommand("play", "Pʟᴀʏ Mᴜsɪᴄ ɪɴ Vᴄ"),
        BotCommand("vplay", "Start streaming requested Video Song"),
        BotCommand("playforce", "Force play your requested song"),
        BotCommand("vplayforce", "Force play your requested Video song"),
        BotCommand("pause", "Pause the current playing stream"),
        BotCommand("resume", "Resume the paused stream"),
        BotCommand("skip", "Skip the current playing stream"),
        BotCommand("end", "End the current stream"),
        BotCommand("player", "Get an interactive player panel"),
        BotCommand("queue", "Show the queued tracks list"),
        BotCommand("auth", "Add a user to auth list"),
        BotCommand("unauth", "Remove a user from the auth list"),
        BotCommand("authusers", "Show list of auth users"),
        BotCommand("cplay", "Start streaming audio on channel"),
        BotCommand("cvplay", "Start streaming video track on channel"),
        BotCommand("channelplay", "Connect channel to group and stream"),
        BotCommand("shuffle", "Shuffle the queue"),
        BotCommand("seek", "Seek stream to given duration"),
        BotCommand("seekback", "Seek backward in stream"),
        BotCommand("speed", "Adjust audio playback speed"),
        BotCommand("loop", "Enable loop for a value"),
        BotCommand("bio", "Enable/Disable Bio Link Protection")  # ✅ Added command
    ])

    # ✅ FIXED plugin import loop (required to load all plugins)
    for all_module in ALL_MODULES:
        if all_module.strip() == "":
            continue
        importlib.import_module(f"DeadlineTech.plugins.{all_module}")

    LOGGER("DeadlineTech.plugins").info("✅ Successfully Imported All Plugins")

    await userbot.start()
    await Anony.start()
    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("DeadlineTech").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass

    await Anony.decorators()
    LOGGER("DeadlineTech").info("✅ DeadlineTech Music Bot Started Successfully")
    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("DeadlineTech").info("🛑 Stopping DeadlineTech Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
