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

    # NÃO use mais: edit = await event.reply("Processing!")

    try:
        if 't.me/+' in link:
            q = await join(userbot, link)
            await Drone.send_message(event.sender_id, str(q))
            return
        
        if 't.me/' in link:
            # -1003922604517 é o ID do seu grupo
            # O 0 indica que não deve haver edição de mensagem
            await get_msg(userbot, Bot, Drone, "-1003922604517", 0, link, 0)
            
    except FloodWait as fw:
        await Drone.send_message(event.sender_id, f'FloodWait: {fw.x} segundos.')
    except Exception as e:
        # Importante: converte o erro para string para evitar avisos de corrotina
        print(f"Erro na clonagem: {str(e)}")
