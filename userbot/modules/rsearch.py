# Copyright (C) 2020 KeselekPermen69
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import datetime
from telethon import events
from asyncio import sleep
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.rsauce(?: |$)(\d*)")
async def _(hentai):
    if hentai.fwd_from:
        return
    link = await hentai.get_reply_message()
    if not link.media:
       await event.edit("```reply to a image/sticker/gif```")
       return
    chat = "@reverseSearchBot"
    await hentai.edit("```Pouring some sauce on it...```")
    async with bot.conversation(chat) as conv:
          try:
              response = conv.wait_event(events.MessageEdited(incoming=True,from_users=648099067))
              msg = await bot.send_file(chat, link.media)
              response = await response
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await hentai.reply("```Please unblock @reverseSearchBot and try again```")
              return
          if response.text.startswith("aaaaah"):
             await hentai.edit("```Too much load.slow down.```")
          else:
             await hentai.delete()
             await bot.send_message(hentai.chat_id, response.message)
             await bot.send_read_acknowledge(hentai.chat_id)
             """ - cleanup chat after completed - """
             await hentai.client.delete_messages(conv.chat_id,
                                                [msg.id, response.id])

CMD_HELP.update({
"rsauce":
"`.rsauce` <to reply>"
"\nUsage: reply to animu media to get sauce"})
