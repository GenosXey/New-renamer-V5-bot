# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
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
from config import Config
from helper.database import digital_botz
from helper.utils import get_seconds, humanbytes
import os, sys, time, asyncio, logging, datetime, pytz, traceback

# pyrogram imports
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await digital_botz.total_users_count()
    if bot.premium:
        total_premium_users = await digital_botz.total_premium_users_count()
    else:
        total_premium_users = "Disabled ✅"
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))    
    start_t = time.time()
    rkn = await message.reply('**Traitement.....**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rkn.edit(text=f"--Statut du bot-- \n\n**⌚️ Temps d'activité du bot :** {uptime} \n**🐌 Ping actuel:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Nombre total d'utilisateurs:** `{total_users}`\n**💸 Nombre total d'utilisateurs premiums:** `{total_premium_users}`")

# bot logs process 
@Client.on_message(filters.command('logs') & filters.user(Config.ADMIN))
async def log_file(b, m):
    try:
        await m.reply_document('BotLog.txt')
    except Exception as e:
        await m.reply(str(e))

@Client.on_message(filters.command(["addpremium", "add_premium"]) & filters.user(Config.ADMIN))
async def add_premium(client, message):
    if not client.premium:
        return await message.reply_text("premium mode disabled ✅")
     
    if client.uploadlimit:
        if len(message.command) < 4:
            return await message.reply_text("Utilisation : /addpremium user_id Type_de_plan (par exemple... Pro, UltraPro) temps (par exemple, '1 jour pour jours', '1 heure pour heures', ou '1 min pour minutes', ou '1 mois pour mois' ou '1 an pour an')", quote=True)

        user_id = int(message.command[1])
        plan_type = message.command[2]

        if plan_type not in ["Pro", "UltraPro"]:
            return await message.reply_text("Type de plan invalide. Veuillez utiliser 'Pro' ou 'UltraPro'.", quote=True)

        time_string = " ".join(message.command[3:])

        time_zone = datetime.datetime.now(pytz.timezone("Africa/Lome"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p")

        user = await client.get_users(user_id)

        if plan_type == "Pro":
            limit = 107374182400
            type = "Pro"
        elif plan_type == "UltraPro":
            limit = 1073741824000
            type = "UltraPro"

        seconds = await get_seconds(time_string)
        if seconds <= 0:
            return await message.reply_text("Format de temps invalide. Veuillez utiliser `/addpremium user_id 1 an 1 mois 1 jour 1 min 10 s`", quote=True)

        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {"id": user_id, "expiry_time": expiry_time}
        await digital_botz.addpremium(user_id, user_data, limit, type)

        user_data = await digital_botz.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0)
        type = user_data.get('usertype', "Free")
        data = await digital_botz.get_user(user_id)
        expiry = data.get("expiry_time")
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")

        await message.reply_text(f"Premium ajouté avec succès ✅\n\n👤 Utilisateur : {user.mention}\n⚡ ID utilisateur : <code>{user_id}</code>\nPlan :- `{type}`\nLimite quotidienne de téléchargement :- `{humanbytes(limit)}`\n⏰ Accès premium : <code>{time_string}</code>\n\n⏳ Date d'adhésion : {current_time}\n\n⌛️ Date d'expiration : {expiry_str_in_ist}", quote=True, disable_web_page_preview=True)

        await client.send_message(
                chat_id=user_id,
                text=f"👋 ʜᴇʏ {user.mention},\nMerci d'avoir acheté le premium.\nProfitez-en !! ✨🎉\n\n⏰ Accès premium : <code>{time}</code>\nᴘʟᴀɴ :- `{type}`\nᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :- `{humanbytes(limit)}`\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True              
            )    

    else:
        if len(message.command) < 3:
            return await message.reply_text("Usage : /addpremium user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')", quote=True)

        user_id = int(message.command[1])
        time_string = " ".join(message.command[2:])

        time_zone = datetime.datetime.now(pytz.timezone("Africa/Lome"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p")

        user = await client.get_users(user_id)        
        seconds = await get_seconds(time_string)
        if seconds <= 0:
            return await message.reply_text("Format de temps invalide. Veuillez utiliser `/addpremium user_id 1 an 1 mois 1 jour 1 min 10 s`", quote=True)

        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {"id": user_id, "expiry_time": expiry_time}
        await digital_botz.addpremium(user_id, user_data)
        data = await digital_botz.get_user(user_id)
        expiry = data.get("expiry_time")
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")

        await message.reply_text(f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_string}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", quote=True, disable_web_page_preview=True)

        await client.send_message(
                chat_id=user_id,
                text=f"👋 ʜᴇʏ {user.mention},\nMerci d'avoir acheté le premium.\nProfitez-en !! ✨🎉\n\n⏰ Accès premium : <code>{time}</code>\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True              
            )    
     

@Client.on_message(filters.command(["removepremium", "remove_premium"]) & filters.user(Config.ADMIN))
async def remove_premium(bot, message):
    if not bot.premium:
        return await message.reply_text("premium mode disabled ✅")
     
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await bot.get_users(user_id)
        if await digital_botz.has_premium_access(user_id):
            await digital_botz.remove_premium(user_id)
            await message.reply_text(f"ʜᴇʏ {user.mention}, Plan premium supprimé avec succès.", quote=True)
            await bot.send_message(chat_id=user_id, text=f"<b>ʜᴇʏ {user.mention},\n\n✨ Votre compte a été retiré de notre plan premium\n\nVérifiez votre plan ici /myplan</b>")
        else:
            await message.reply_text("Impossible de retirer l'utilisateur premium !\nÊtes-vous sûr que c'était un ID d'utilisateur premium ? ?", quote=True)
    else:
        await message.reply_text("Utilisation : /remove_premium ID utilisateur", quote=True)


# Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    rkn = await b.send_message(text="**🔄 Processus arrêté. Le bot redémarre......**", chat_id=m.chat.id)
    failed = 0
    success = 0
    deactivated = 0
    blocked = 0
    start_time = time.time()
    total_users = await digital_botz.total_users_count()
    all_users = await digital_botz.get_all_users()
    async for user in all_users:
        try:
            restart_msg = f"ʜᴇʏ, {(await b.get_users(user['_id'])).mention}\n\n**🔄 Processus arrêté. Le bot redémarre......\n\n✅️ 🔄 Le bot a été redemarré. Vous pouvez M'utilisé..**"
            await b.send_message(user['_id'], restart_msg)
            success += 1
        except InputUserDeactivated:
            deactivated +=1
            await digital_botz.delete_user(user['_id'])
        except UserIsBlocked:
            blocked +=1
            await digital_botz.delete_user(user['_id'])
        except Exception as e:
            failed += 1
            await digital_botz.delete_user(user['_id'])
            print(e)
            pass
        try:
            await rkn.edit(f"<u>Redémarrage en cours:</u>\n\n• Nombre total d'utilisateurs: {total_users}\n• Réussi: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
    completed_restart = datetime.timedelta(seconds=int(time.time() - start_time))
    await rkn.edit(f"ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʀᴇsᴛᴀʀᴛ: {completed_restart}\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.ADMIN))
async def ban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\n"
            f"Usage:\n\n"
            f"`/ban user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban 1234567 28 You misused me.`\n"
            f"This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(user_id,              
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n"
                f"**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await digital_botz.ban_user(user_id, ban_duration, ban_reason)
        await m.reply_text(ban_log_text, quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.ADMIN))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.\n\n"
            f"Usage:\n\n`/unban user_id`\n\n"
            f"Eg: `/unban 1234567`\n"
            f"This will unban user with id `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await digital_botz.remove_ban(user_id)
        await m.reply_text(unban_log_text, quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occurred! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("banned_users") & filters.user(Config.ADMIN))
async def _banned_users(_, m: Message):
    all_banned_users = await digital_botz.get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)

     
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......")
    all_users = await digital_botz.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ..!") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await digital_botz.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await digital_botz.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ `{completed_in}`.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
 

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
