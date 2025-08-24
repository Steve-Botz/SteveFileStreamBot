import re
from os import environ, getenv
from typing import Set, Optional, List, Dict
from Script import script

SESSION = environ.get('SESSION', 'Webavbot')

API_ID = int(environ.get('API_ID', ''))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')

BIN_CHANNEL = int(environ.get("BIN_CHANNEL", '-1002456017788'))
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", '-1002421781174'))
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", '-1002464620680'))
VERIFIED_LOG = int(environ.get('VERIFIED_LOG', '-1002317782023'))

ADMINS = list(map(int, environ.get('ADMINS', '6317211079').split()))
AUTH_CHANNEL = list(map(int, environ.get("AUTH_CHANNEL", "-1002553442366").split()))

OWNER_USERNAME = environ.get("OWNER_USERNAME", 'AmaniContactBot')
BOT_USERNAME = environ.get("BOT_USERNAME", '')

CHANNEL = environ.get('CHANNEL', 'https://t.me/steveBotz')
SUPPORT = environ.get('SUPPORT', 'https://t.me/SteveBotzSupport')
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', 'https://t.me/SteveBotzSupport')
HOW_TO_OPEN = environ.get('HOW_TO_OPEN', 'https://t.me/SteveBotzSupport')

# ✅ Feature Toggles (True/False)
VERIFY = environ.get("VERIFY", False)  # Enable user verification
FSUB = environ.get("FSUB", True)  # Force Subscribe feature
ENABLE_LIMIT = environ.get("ENABLE_LIMIT", True)  # Enable file limits
BATCH_VERIFY = environ.get("BATCH_VERIFY", False)  # Verify files in batch
IS_SHORTLINK = bool(environ.get('IS_SHORTLINK', False))  # Enable channel shortlink creation
MAINTENANCE_MODE = environ.get("MAINTENANCE_MODE", False)  # Put bot in maintenance
PROTECT_CONTENT = environ.get('PROTECT_CONTENT', False)  # Enable content protection
PUBLIC_FILE_STORE = environ.get('PUBLIC_FILE_STORE', False)  # Public or private file visibility
BATCH_PROTECT_CONTENT = environ.get('BATCH_PROTECT_CONTENT', False)  # Batch file protection

SHORTLINK_URL = environ.get('SHORTLINK_URL', 'techvjlink.site')
SHORTLINK_API = environ.get('SHORTLINK_API', 'd73e70a35dc3877fa14afbf51fa8ec312c94780c')

DB_URL = environ.get('DATABASE_URI', "")
DB_NAME = environ.get('DATABASE_NAME', "Cluster0")

# 📸 all Media (Images)
QR_CODE = environ.get('QR_CODE', 'https://graph.org/file/6afb4093d5ec5c4176979.jpg')
VERIFY_IMG = environ.get("VERIFY_IMG", "https://graph.org/file/1669ab9af68eaa62c3ca4.jpg")
AUTH_PICS = environ.get('AUTH_PICS', 'https://telegra.ph/file/4f314c2d9fcb797ad9c2c-113d486f43d401d4c2.jpg')
PICS = environ.get('PICS', 'https://telegra.ph/file/5e45649361713e00c90e6-e53b35687247f575cf.jpg')
FILE_PIC = environ.get('FILE_PIC', 'https://telegra.ph/file/00ecffd7518e788eb8b4a-8e29883c2080ef1117.jpg') 

# 📝 File Captions
FILE_CAPTION = environ.get('FILE_CAPTION', f"{script.CAPTION}")  # Caption for single file
BATCH_FILE_CAPTION = environ.get('BATCH_FILE_CAPTION', f"{script.CAPTION}")  # Caption for batch files
CHANNEL_FILE_CAPTION = environ.get('CHANNEL_FILE_CAPTION', f"{script.CAPTION}")  # Caption for channel posts

# ⏱️ Time & Rate Limit Settings
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # Ping interval in seconds (20 minutes)
SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))  # Threshold for sleep delay
RATE_LIMIT_TIMEOUT = int(environ.get("RATE_LIMIT_TIMEOUT", "500"))  # Rate limit time (10 mins)
MAX_FILES = int(environ.get("MAX_FILES", "10"))  # Max files allowed per user
VERIFY_EXPIRE = int(environ.get('VERIFY_EXPIRE', 60))  # Time (in hours) after which verification expires

# ⚙️ Worker Configuration
WORKERS = int(getenv('WORKERS', '4'))  # Number of async workers
MULTI_CLIENT = False  # Enable multi-client handling (if needed)

# 🔧 App/Heroku Configuration
name = str(environ.get('name', 'avbotz'))  # Project name
APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))  # Heroku app name (optional)
else:
    ON_HEROKU = False

# 🌐 Server Settings
PORT = int(getenv('PORT', '2626'))  # Port for web server
NO_PORT = str(getenv("NO_PORT", True)).lower() in ("true", "1", "yes")  # Disable port in URL
HAS_SSL = str(getenv("HAS_SSL", True)).lower() in ("true", "1", "yes")  # Use HTTPS if True
BIND_ADDRESS = getenv("WEB_SERVER_BIND_ADDRESS", "127.0.0.1")  # Server bind address
FQDN = getenv("FQDN", "") or BIND_ADDRESS  # Full domain name or fallback to bind address
PORT_SEGMENT = "" if NO_PORT else f":{PORT}"  # Port in URL if not disabled
PROTOCOL = "https" if HAS_SSL else "http"  # Protocol for URL
URL = f"{PROTOCOL}://{FQDN}{PORT_SEGMENT}"  # Final generated base URL
