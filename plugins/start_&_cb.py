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

    # ✅ Send sticker before start message
    await message.reply_sticker("CAACAgUAAxkBAAIE4Gf6qY1590UCET8-25D_Mi5OsSduAAImCQACzoAZVchVZroLpXfgHgQ")

    user = message.from_user
    await digital_botz.add_user(client, message) 
    if Config.RKN_PIC:
        await message.reply_photo(Config.RKN_PIC, caption=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button))    
    else:
        await message.reply_text(text=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button), disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command("myplan"))
async def myplan(client, message):
    if not client.premium:
        return # premium mode disabled ✓

    user_id = message.from_user.id
    user = message.from_user.mention

    if await digital_botz.has_premium_access(user_id):
        data = await digital_botz.get_user(user_id)
        expiry_str_in_ist = data.get("expiry_time")
        time_left_str = expiry_str_in_ist - datetime.datetime.now()

        text = f"ᴜˢᴇʀ :- {user}\nᴜˢᴇʀ ɪᴅ :- <code>{user_id}</code>\n"

        if client.uploadlimit:
            await digital_botz.reset_uploadlimit_access(user_id)                
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")

            text += f"ᴘʟᴀɴ :- `{type}`\nᴅᴀɪʟʏ ᴜᴹʟᴏᴀᴅ ʟɪᴛ :- `{humanbytes(limit)}`\nᴝʏᴍʏ ᴜʀᴇᴅ :- `{humanbytes(used)}`\nʁᴇᴛᴀɪɴ :- `{humanbytes(remain)}`\n"

        text += f"ᴛɪᴍᴇ ʟᴇɿᴛ : {time_left_str}\nᴇᴀᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}"

        await message.reply_text(text, quote=True)

    else:
        if client.uploadlimit:
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")

            text = f"ᴜˢᴇʀ :- {user}\nᴜˢᴇʀ ɪᴅ :- <code>{user_id}</code>\nᴘʟᴀɴ :- `{type}`\nᴅᴀɪʟʏ ᴜᴹʟᴏᴀᴅ ʟɪᴛ :- `{humanbytes(limit)}`\nᴝʏᴍʏ ᴜʀᴇᴅ :- `{humanbytes(used)}`\nʁᴇᴛᴀɪɴ :- `{humanbytes(remain)}`\nᴇᴘɪʀᴇᴄ ᴅᴀᴛᴇ :- ʟɪᴟᴟᴇᴝᴇ"

            await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 Vérifier les plans premium 💸", callback_data='upgrade')]]), quote=True)

        else:
            m=await message.reply_sticker("CAACAgIAAxkBAAIBTGVjQbHuhOiboQsDm35brLGyLQ28AAJ-GgACglXYSXgCrotQHjibHgQ")
            await message.reply_text(f"Hey {user},\n\nVous n'avez pas de plans premium actifs. Si vous souhaitez souscrire à un plan premium, cliquez sur le bouton ci-dessous. 👇",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 Vérifier les plans premium 💸", callback_data='upgrade')]]))			 
            await asyncio.sleep(2)
            await m.delete()
