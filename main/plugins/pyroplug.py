#Github.com-Vasusen-code

import asyncio, time, os

from .. import bot as Drone
from main.plugins.progress import progress_for_pyrogram
from main.plugins.helpers import screenshot

from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from ethon.pyfunc import video_metadata
from ethon.telefunc import fast_upload
from telethon.tl.types import DocumentAttributeVideo
from telethon import events

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def get_msg(userbot, client, bot, sender, edit_id, msg_link, i):
    """ userbot: PyrogramUserBot | client: PyrogramBotClient | bot: TelethonBotClient """
    try:
        # Varre os últimos 50 diálogos para achar o ID e atualizar o Access Hash
        async for dialog in userbot.get_dialogs(limit=50):
            if dialog.chat.id == sender:
                print(f"Chat encontrado e validado: {dialog.chat.title}")
                break
    except Exception as e:
        print(f"Erro ao varrer diálogos: {e}")
    # Validação inicial do edit_id para evitar erros de Peer/Message ID
    use_edit = True if edit_id and edit_id != 0 else False
    edit = None
    chat = ""
    round_message = False
    
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    
    msg_id = int(msg_link.split("/")[-1]) + int(i)
    height, width, duration, thumb_path = 90, 90, 0, None
    
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        if 't.me/b/' in msg_link:
            chat = str(msg_link.split("/")[-2])
        else:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        
        file = ""
        try:
            msg = await userbot.get_messages(chat, msg_id)
            
            # Caso seja apenas texto/link
            if not msg.media or msg.media == MessageMediaType.WEB_PAGE:
                if msg.text:
                    if use_edit: edit = await client.edit_message_text(sender, edit_id, "Cloning...")
                    await client.send_message(sender, msg.text.markdown)
                    if use_edit and edit: await edit.delete()
                    return

            # Início do Download
            if use_edit: edit = await client.edit_message_text(sender, edit_id, "Trying to Download...")
            
            file = await userbot.download_media(
                msg,
                progress=progress_for_pyrogram,
                progress_args=(client, "**DOWNLOADING:**\n", edit, time.time()) if use_edit else (client, "Downloading...", None, time.time())
            )
            
            if use_edit and edit: await edit.edit('Preparing to Upload!')
            
            caption = msg.caption if msg.caption is not None else ""
            
            # Tratamento de Vídeo Nota (Round)
            if msg.media == MessageMediaType.VIDEO_NOTE:
                round_message = True
                data = video_metadata(file)
                height, width, duration = data["height"], data["width"], data["duration"]
                try:
                    thumb_path = await screenshot(file, duration, sender)
                except:
                    thumb_path = None
                
                await userbot.send_video_note(
                    chat_id=sender,
                    video_note=file,
                    length=height, duration=duration, 
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(client, '**UPLOADING:**\n', edit, time.time()) if use_edit else (client, "Uploading...", None, time.time())
                )
            
            # Tratamento de Vídeo
            elif msg.media == MessageMediaType.VIDEO:
                data = video_metadata(file)
                height, width, duration = data["height"], data["width"], data["duration"]
                try:
                    thumb_path = await screenshot(file, duration, sender)
                except:
                    thumb_path = None
                
                await userbot.send_video(
                    chat_id=sender,
                    video=file,
                    caption=caption,
                    supports_streaming=True,
                    height=height, width=width, duration=duration, 
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(client, '**UPLOADING:**\n', edit, time.time()) if use_edit else (client, "Uploading...", None, time.time())
                )
            
            elif msg.media == MessageMediaType.PHOTO:
                if use_edit and edit: await edit.edit("Uploading photo...")
                await bot.send_file(sender, file, caption=caption)
            
            else:
                thumb_path = thumbnail(sender)
                await userbot.send_document(
                    sender, file, caption=caption, thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(client, '**UPLOADING:**\n', edit, time.time()) if use_edit else (client, "Uploading...", None, time.time())
                )

            if use_edit and edit: await edit.delete()

        except Exception as e:
            print(f"Error: {e}")
            if use_edit:
                try: await client.edit_message_text(sender, edit_id, f"Failed: {str(e)}")
                except: pass
        finally:
            if file and os.path.exists(file):
                os.remove(file)
    else:
        # Lógica para links públicos t.me/canal/123
        if use_edit: edit = await client.edit_message_text(sender, edit_id, "Cloning...")
        chat = msg_link.split("t.me")[1].split("/")[1]
        try:
            await client.copy_message(sender, chat, msg_id)
            if use_edit and edit: await edit.delete()
        except Exception as e:
            if use_edit: await client.edit_message_text(sender, edit_id, f"Error: {e}")

async def get_bulk_msg(userbot, client, sender, msg_link, i):
    x = await client.send_message(sender, "Processing!")
    await get_msg(userbot, client, Drone, sender, x.id, msg_link, i)
