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

# imports
from pyrogram import Client, filters 
from helper.database import digital_botz

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    rkn = await message.reply_text("__**Veuillez patienter**__")
    if len(message.command) == 1:
       return await rkn.edit("**__Donnez la légende__\n\nExemple:- `/set_caption {filename}\n\n💾 Poids: {filesize}\n\n⏰ Durée: {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await digital_botz.set_caption(message.from_user.id, caption=caption)
    await rkn.edit("__**✅ Légende enregistrée**__")
   
@Client.on_message(filters.private & filters.command(['del_caption', 'delete_caption', 'delcaption']))
async def delete_caption(client, message):
    rkn = await message.reply_text("__**Veuillez patienter**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if not caption:
       return await rkn.edit("__**😔 Vous n'avez pas de légende**__")
    await digital_botz.set_caption(message.from_user.id, caption=None)
    await rkn.edit("__**❌️ Légende supprimée**__")
                                       
@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    rkn = await message.reply_text("__**Veuillez patienter**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if caption:
       await rkn.edit(f"**Votre légende:-**\n\n`{caption}`")
    else:
       await rkn.edit("__**😔 Vous n'avez pas de légende.**__")

@Client.on_message(filters.private & filters.command(['view_thVous n'avez pas de légende.umb', 'viewthumb']))
async def viewthumb(client, message):
    rkn = await message.reply_text("__**Veuillez patienter**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
        await rkn.delete()
    else:
        await rkn.edit("😔 __**Vous n'avez pas de miniature**__") 
		
@Client.on_message(filters.private & filters.command(['del_thumb', 'delete_thumb', 'delthumb']))
async def removethumb(client, message):
    rkn = await message.reply_text("__**Veuillez patienter**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await digital_botz.set_thumbnail(message.from_user.id, file_id=None)
        await rkn.edit("❌️ __**Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ**__")
        return
    await rkn.edit("😔 __**Vous n'avez pas de miniature**__")


@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    rkn = await message.reply_text("__**Veuillez patienter**__")
    await digital_botz.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await rkn.edit("✅️ __**Miniature enregistrée**__")

# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support
