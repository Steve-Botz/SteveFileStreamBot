from pyrogram import Client, filters
from pyrogram.types import *
from Script import script
from database.users_db import db
from info import ADMINS, PREMIUM_LOGS
from datetime import timedelta
import pytz, datetime, time, asyncio
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p") 
        user_id = int(message.command[1])  
        try:
            user = await client.get_users(user_id)
        except:
            await message.reply_text("Invalid user ID")
            return
            
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  
            await db.update_user(user_data) 
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")
            expiry_str_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y 𝘈𝘵 : %I:%M:%S %p")         
            await message.reply_text(f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True)
            try:
                await client.send_message(
                    chat_id=user_id,
                    text=f"🎉 𝘊𝘰𝘯𝘨𝘳𝘢𝘵𝘶𝘭𝘢𝘵𝘪𝘰𝘯𝘴! 𝘠𝘰𝘶'𝘷𝘦 𝘨𝘰𝘵 𝘗𝘳𝘦𝘮𝘪𝘶𝘮 𝘈𝘤𝘤𝘦𝘴𝘴!\n\n⏳ 𝘋𝘶𝘳𝘢𝘵𝘪𝘰𝘯 : {time}\n📅 𝘌𝘹𝘱𝘪𝘳𝘺 : {expiry_str_ist}\n\n✨ 𝘌𝘯𝘫𝘰𝘺 𝘺𝘰𝘶𝘳 𝘱𝘳𝘦𝘮𝘪𝘶𝘮 𝘣𝘦𝘯𝘦𝘧𝘪𝘵𝘴!", disable_web_page_preview=True             
                )    
            except:
                pass
                
            await client.send_message(PREMIUM_LOGS, text=f"#Added_Premium\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True)
                    
        else:
            await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year'")
    else:
        await message.reply_text("Usage : /add_premium user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')")

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        try:
            user = await client.get_users(user_id)
        except:
            await message.reply_text("Invalid user ID")
            return
            
        if await db.remove_premium_access(user_id):
            await message.reply_text("ᴜꜱᴇʀ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ !")
            try:
                await client.send_message(
                    chat_id=user_id,
                    text=f"<b>ʜᴇʏ {user.mention},\n\n𝒀𝒐𝒖𝒓 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑨𝒄𝒄𝒆𝒔𝒔 𝑯𝒂𝒔 𝑩𝒆𝒆𝒏 𝑹𝒆𝒎𝒐𝒗𝒆𝒅. 𝑻𝒉𝒂𝒏𝒌 𝒀𝒐𝒖 𝑭𝒐𝒓 𝑼𝒔𝒊𝒏𝒈 𝑶𝒖𝒓 𝑺𝒆𝒓𝒗𝒊𝒄𝒆 😊. 𝑪𝒍𝒊𝒄𝒌 𝑶𝒏 /buy 𝑻𝒐 𝑪𝒉𝒆𝒄𝒌 𝑶𝒖𝒕 𝑶𝒕𝒉𝒆𝒓 𝑷𝒍𝒂𝒏𝒔.\n\n<blockquote>आपका Premium Access हटा दिया गया है। हमारी सेवा का उपयोग करने के लिए धन्यवाद 🥳 हमारी अन्य योजनाओं की जाँच करने के लिए /plan पर क्लिक करें ।</blockquote></b>"
                )
            except:
                pass
        else:
            await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴜꜱᴇʀ !\nᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ, ɪᴛ ᴡᴀꜱ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ɪᴅ ?")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /remove_premium user_id")

@Client.on_message(filters.command("premium_user") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("Fetching ...")  
    users = await db.get_all_users()
    users_list = []
    async for user in users:
        users_list.append(user)    
    user_data = {user['id']: await db.get_user(user['id']) for user in users_list}    
    new_users = []
    for user in users_list:
        user_id = user['id']
        data = user_data.get(user_id)
        expiry = data.get("expiry_time") if data else None        
        if expiry:
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y %I:%M:%S %p")          
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days, remainder = divmod(time_left.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)            
            time_left_str = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"            
            user_info = await client.get_users(user_id)
            user_str = (
                f"{len(new_users) + 1}. User ID: {user_id}\n"
                f"Name: {user_info.mention}\n"
                f"Expiry Date: {expiry_str_in_ist}\n"
                f"Expiry Time: {time_left_str}\n\n"
            )
            new_users.append(user_str)
    new = "Paid Users - \n\n" + "\n".join(new_users)   
    try:
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")

