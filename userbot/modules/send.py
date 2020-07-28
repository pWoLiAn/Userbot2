#BY ME huuhuuhu
 
import datetime
from telethon import events
from telethon import utils
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register
 
@register(outgoing=True, pattern="^.send (.*)")
async def _(hentai):
    if hentai.fwd_from:
        return
    chat = str(hentai.pattern_match.group(1).split(' ', 1)[0])
    link = str(hentai.pattern_match.group(1).split(' ', 1)[1])
    if not link:
        return await hentai.edit("`I can't search nothing`")
     
    botid = await hentai.client.get_entity(chat)
    await hentai.edit("```Processing```")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=botid))
              msg = await bot.send_message(chat, link)
              response = await response
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError: 
              await hentai.reply(f"`Please unblock` {chat} `and try again`")
              return
         
          await hentai.edit(f"`Message sent` : {link}"
                               f"\n`Sent to` : {chat}")
          await bot.send_message(hentai.chat_id, response.message)
          await bot.send_read_acknowledge(hentai.chat_id)
          """ - cleanup chat after completed - """
          await hentai.client.delete_messages(conv.chat_id,
                                                [msg.id, response.id])
    
CMD_HELP.update({
"sendbot": 
"`.send` <@bot_username> <cmd. to send>"
"\nUsage: Send cmd to bot and forwards the output"})
