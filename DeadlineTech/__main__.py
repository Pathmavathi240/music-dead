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
    # ✅ Setup global crash handler
    setup_global_exception_handler()

    # ✅ Ensure assistant clients are configured
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("❌ Assistant client variables not defined, exiting...")
        exit()

    # ✅ Load banned users
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"⚠️ Failed to fetch banned users: {e}")

    # ✅ Start bot
    await app.start()

    # ✅ Set bot commands
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
        BotCommand("bio", "Enable/Disable Bio Link Protection")  # ✅ Custom command
    ])

    # ✅ Import all plugin modules safely
    for all_module in ALL_MODULES:
        all_module = all_module.strip()
        if not all_module:
            continue
        try:
            importlib.import_module(f"DeadlineTech.plugins.{all_module}")
        except Exception as e:
            LOGGER("Plugin Import").error(f"❌ Failed to import plugin '{all_module}': {e}")

    LOGGER("DeadlineTech.plugins").info("✅ Successfully Imported All Plugins")

    # ✅ Start assistant userbot
    await userbot.start()
    await Anony.start()

    # ✅ Attempt dummy stream to ensure group call works
    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("DeadlineTech").error(
            "❌ Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except Exception as e:
        LOGGER("DeadlineTech").warning(f"⚠️ Failed to stream test video: {e}")

    await Anony.decorators()

    LOGGER("DeadlineTech").info("✅ DeadlineTech Music Bot Started Successfully")
    await idle()

    # ✅ Shutdown sequence
    await app.stop()
    await userbot.stop()
    LOGGER("DeadlineTech").info("🛑 Stopping DeadlineTech Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
