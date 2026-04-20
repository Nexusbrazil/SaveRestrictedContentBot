#Github.com/Vasusen-code

import time, os

from .. import bot as Drone
from .. import userbot, Bot
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_msg
from main.plugins.helpers import get_link, join

from telethon import events
from pyrogram.errors import FloodWait

from ethon.telefunc import force_sub

fs = None

ft = f"To use this bot you've to join @{fs}."

message = "Send me the message link you want to start saving from, as a reply to this message."

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return
    try:
        link = get_link(event.text)
        if not link:
            return
    except TypeError:
        return
    #s, r = await force_sub(event.client, fs, event.sender_id, ft)
    #if s == True:
    #    await event.reply(r)
    #   return
    #edit = await event.reply("Processing!")
    try:
        if 't.me/+' in link:
            q = await join(userbot, link)
            await Drone.send_message(event.sender_id, str(q))
            return
        if 't.me/' in link:
            await get_msg(userbot, Bot, Drone, "-1003922604517", 0, link, 0)
    except FloodWait as fw:
        await Drone.send_message(event.sender_id, f'FloodWait: {fw.x} segundos.')
    except Exception as e:
        # Usamos apenas o print para o log do Railway para evitar o erro de corrotina no envio
        print(f"Erro na clonagem do link {link}: {e}")
    
