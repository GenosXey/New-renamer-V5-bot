# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
"""
Apache License 2.0
Copyright (c) 2022 @Digital_Botz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Telegram Link : https://t.me/Digital_Botz 
Repo Link : https://github.com/DigitalBotz/Digital-Rename-Bot
License Link : https://github.com/DigitalBotz/Digital-Rename-Bot/blob/main/LICENSE
"""

# extra imports
import random, asyncio, datetime, pytz, time, psutil, shutil

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery

# bots imports
from helper.database import digital_botz
from config import Config, rkn
from helper.utils import humanbytes
from plugins import __version__ as _bot_version_, __developer__, __database__, __library__, __language__, __programer__

upgrade_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('Acheter Premium ✓', user_id=int(6705898491)),
         ],[
        InlineKeyboardButton("Retour", callback_data = "start")
]])

upgrade_trial_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('Acheter Premium ✓', user_id=int(6705898491)),
         ],[
        InlineKeyboardButton("Essai - 12 heures ✓", callback_data = "give_trial"),
        InlineKeyboardButton("Retour", callback_data = "start")
]])

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    start_button = [[        
        InlineKeyboardButton('Mises à jour', url='https://t.me/BotZFlix'),
        InlineKeyboardButton('Support', url='https://t.me/BotZFlixSupport')
        ],[
        InlineKeyboardButton('À propos', callback_data='about'),
        InlineKeyboardButton('Aide', callback_data='help')       
         ]]
        
    if client.premium:
        start_button.append([InlineKeyboardButton('💸 Mettre à niveau vers premium 💸', callback_data='upgrade')])

    # ✅ Affiche tous les stickers l’un après l’autre puis les supprime
    stickers = [
        "CAACAgUAAxkBAAIE4Gf6qY1590UCET8-25D_Mi5OsSduAAImCQACzoAZVchVZroLpXfgHgQ",
        "CAACAgUAAxkBAAIFOGf7e3t7xbexqML4lUBov33y0fwWAALgCAACW_HQVoT7skQi0IBNHgQ",
        "CAACAgUAAxkBAAIFPGf7e32N9GQtxFUBhRpnBcdq-n2VAAIUCwACrZTRViZ7bFXnR26eHgQ",
        "CAACAgUAAxkBAAIFQGf7e4BWBoddo5yVau4uEnW05RtbAAKLCwACwurRVj5eDbteWRIYHgQ",
        "CAACAgUAAxkBAAIFRGf7e4JmicaVg9hMejExAlZj778PAAITCAACVknZVofykXMFYuv7HgQ"
    ]

    for sticker_id in stickers:
        sent = await message.reply_sticker(sticker_id)
        await asyncio.sleep(1.5)
        await sent.delete()

    user = message.from_user
    await digital_botz.add_user(client, message) 
    if Config.RKN_PIC:
        await message.reply_photo(
            Config.RKN_PIC,
            caption=rkn.START_TXT.format(user.mention),
            reply_markup=InlineKeyboardMarkup(start_button),
            parse_mode="HTML"
        )
    else:
        await message.reply_text(
            text=rkn.START_TXT.format(user.mention),
            reply_markup=InlineKeyboardMarkup(start_button),
            disable_web_page_preview=True,
            parse_mode="HTML"
        )
