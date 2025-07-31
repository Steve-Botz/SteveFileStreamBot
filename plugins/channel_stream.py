import asyncio
import os
import random
from web.utils.file_properties import get_hash
from pyrogram import Client, filters, enums
from info import BIN_CHANNEL, URL, CHANNEL, BOT_USERNAME, IS_SHORTLINK, CHANNEL_FILE_CAPTION, HOW_TO_OPEN
from utils import get_size, get_shortlink
from Script import script
from database.users_db import db
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Queue for processing messages
processing_queue = asyncio.Queue()
worker_task = None

async def process_queue():
    """Worker function to process messages from the queue"""
    global worker_task
    while True:
        try:
            bot, broadcast = await processing_queue.get()
            await process_broadcast(bot, broadcast)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Queue worker error: {e}")
        finally:
            processing_queue.task_done()

async def process_broadcast(bot: Client, broadcast: Message):
    """Process individual broadcast message"""
    try:
        chat_id = broadcast.chat.id
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
        
        file = broadcast.document or broadcast.video
        file_name = file.file_name if file else "Unknown File"
        
        # Forward to bin channel
        msg = await broadcast.forward(BIN_CHANNEL)
        
        # Generate links
        raw_stream = f"{URL}watch/{msg.id}/SteveBotz.mkv?hash={get_hash(msg)}"
        raw_download = f"{URL}{msg.id}?hash={get_hash(msg)}"
        raw_file_link = f"https://t.me/{BOT_USERNAME}?start=file_{msg.id}"
        
        if IS_SHORTLINK:
            stream = await get_shortlink(raw_stream)
            download = await get_shortlink(raw_download)
            file_link = await get_shortlink(raw_file_link)
        else:
            stream = raw_stream
            download = raw_download
            file_link = raw_file_link
        
        # Log in bin channel
        await msg.reply_text(
            text=f"**Channel:** `{broadcast.chat.title}`\n**ID:** `{broadcast.chat.id}`\n**Stream URL:** {stream}",
            quote=True
        )
        
        # Create buttons
        buttons_list = [
            [InlineKeyboardButton("🔺 ꜱᴛʀᴇᴀᴍ", url=stream),
             InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 🔻", url=download)]
           # [InlineKeyboardButton('• ɢᴇᴛ ғɪʟᴇ •', url=file_link)]
        ]
        
        if IS_SHORTLINK:
            buttons_list.append([InlineKeyboardButton("• ʜᴏᴡ ᴛᴏ ᴏᴘᴇɴ •", url=HOW_TO_OPEN)])
        
        buttons = InlineKeyboardMarkup(buttons_list)
        
        # Send new message with links instead of editing caption
        await bot.send_message(
            chat_id=chat_id,
            text=CHANNEL_FILE_CAPTION.format(CHANNEL, file_name),
            reply_to_message_id=broadcast.id,
            reply_markup=buttons,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        print(f"Error processing message: {e}")
        await bot.send_message(
            BIN_CHANNEL, 
            f"❌ **Error in channel {broadcast.chat.id}:** `{e}`", 
            disable_web_page_preview=True
        )

@Client.on_message(filters.channel & (filters.document | filters.video) & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot: Client, broadcast: Message):
    """Handler for channel messages"""
    global worker_task
    
    # Start worker if not running
    if worker_task is None or worker_task.done():
        worker_task = asyncio.create_task(process_queue())
    
    # Add message to processing queue
    await processing_queue.put((bot, broadcast))
