from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    MBUTTON = [
        [
            InlineKeyboardButton("• ғᴏɴᴛ •", callback_data="mplus HELP_Font"),
            InlineKeyboardButton("• ᴛ-ɢʀᴀᴘʜ •", callback_data="mplus HELP_TG"),
            
        ],
        [
            InlineKeyboardButton("<", callback_data=f"settings_back_helper"),
            InlineKeyboardButton(">", callback_data=f"managebot123 settings_back_helper"),
        ]
    ]
