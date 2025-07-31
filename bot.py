import os, sys, glob, pytz, asyncio, logging, importlib, time
from pathlib import Path
from pyrogram import idle
from aiohttp import web, ClientSession

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)
 
from info import *
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from web import web_server, check_expired_premium
from web.server import Webavbot
from utils import temp, ping_server
from web.server.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
Webavbot.start()
loop = asyncio.get_event_loop()

async def koyeb_ping():
    while True:
        await asyncio.sleep(30)
        try:
            async with ClientSession() as session:
                start_time = time.time()
                async with session.get(URL) as resp:
                    if resp.status == 200:
                        elapsed = (time.time() - start_time) * 1000
                        logging.info(f"Ping Successful ✅ | Status: {resp.status} | Response Time: {elapsed:.2f}ms")
                    else:
                        logging.warning(f"Ping Received Unexpected Status: {resp.status}")
        except Exception as e:
            logging.error(f"Ping Failed ❌: {str(e)}")

async def start():
    print('\n')
    print('Initalizing Your Bot')
    bot_info = await Webavbot.get_me()
    await initialize_clients()
    
    asyncio.create_task(koyeb_ping())
    
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
            
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    me = await Webavbot.get_me()
    temp.BOT = Webavbot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    Webavbot.loop.create_task(check_expired_premium(Webavbot))
    await Webavbot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    await Webavbot.send_message(chat_id=ADMINS[0] ,text='<b>ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ !!</b>')
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('----------------------- Service Stopped -----------------------')
