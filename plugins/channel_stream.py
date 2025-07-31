import asyncio
import random
from web.utils.file_properties import get_hash
from pyrogram import Client, filters, enums
from info import BIN_CHANNEL, URL, CHANNEL, BOT_USERNAME, IS_SHORTLINK, HOW_TO_OPEN
from utils import get_shortlink
from database.users_db import db
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.channel & (filters.document | filters.video) & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot: Client, broadcast: Message):
    try:
        chat_id = broadcast.chat.id
        
        # Handle channel ban check
        if str(chat_id).startswith("-100"):
            if await db.is_channel_blocked(chat_id):
                try:
                    await bot.send_message(
                        chat_id,
                        "🚫 **This channel is banned from using the bot.**\n\n"
                        "🔄 **Contact admin if you think this is a mistake.**\n\n@AV_OWNER_BOT"
                    )
                except:
                    pass
                await bot.leave_chat(chat_id)
                return

        # Generate file links before forwarding
        file_id = f"{random.randint(1000000000, 9999999999)}"
        raw_stream = f"{URL}watch/{file_id}/avbotz.mkv?hash={get_hash(file_id)}"
        raw_download = f"{URL}{file_id}?hash={get_hash(file_id)}"
        raw_file_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"

        # Create buttons
        buttons_list = [
            [InlineKeyboardButton("🔺 ꜱᴛʀᴇᴀᴍ", url=await get_shortlink(raw_stream) if IS_SHORTLINK else raw_stream),
             InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 🔻", url=await get_shortlink(raw_download) if IS_SHORTLINK else raw_download)]
         #   [InlineKeyboardButton('• ᴄʜᴇᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ғɪʟᴇ •', url=await get_shortlink(raw_file_link) if IS_SHORTLINK else raw_file_link)]
        ]
        
        if IS_SHORTLINK:
            buttons_list.append([
                InlineKeyboardButton("• ʜᴏᴡ ᴛᴏ ᴏᴘᴇɴ •", url=HOW_TO_OPEN)
            ])
            
        buttons = InlineKeyboardMarkup(buttons_list)

        # Add buttons to original message
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=buttons
        )

        # Forward to bin channel after adding buttons
        msg = await broadcast.forward(BIN_CHANNEL)
        await msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n"
                 f"**CHANNEL ID:** `{broadcast.chat.id}`\n"
                 f"**File ID:** `{file_id}`",
            quote=True
        )

    except asyncio.exceptions.TimeoutError:
        await asyncio.sleep(5)
        await channel_receive_handler(bot, broadcast)

    except FloodWait as w:
        await asyncio.sleep(w.value)

    except Exception as e:
        print(f"Error processing file: {e}")
        await bot.send_message(
            BIN_CHANNEL,
            f"❌ **Channel Handler Error:**\n`{e}`",
            disable_web_page_preview=True
        )
