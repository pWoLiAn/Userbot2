# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing userid, chatid and log commands"""

from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj


@register(outgoing=True, pattern="^.userid$")
async def useridgetter(target):
    """ For .userid command, returns the ID of the target user. """
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**Name:** {} \n**User ID:** `{}`".format(
            name, user_id))


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def permalink(mention):
    """ For .link command, generates a link to the user's PM with a custom text. """
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = user.first_name.replace("\u2060",
                                      "") if user.first_name else user.username
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ For .chatid, returns the ID of the chat you are in at that moment. """
    await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):
    """ For .log command, forwards a message or the command argument to the bot logs group """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`What am I supposed to log?`")
            return
        await log_text.edit("`Logged Successfully`")
    else:
        await log_text.edit("`This feature requires Logging to be enabled!`")
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ Basically it's .kickme command """
    await leave.edit("`Kicked myself LoL`")
    await sleep(2)
    await leave.delete()
    await leave.client.kick_participant(leave.chat_id, 'me')


@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ For .unmutechat command, unmute a muted chat. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        await unm_e.edit('`Running on Non-SQL Mode!`')
        return
    unkread(str(unm_e.chat_id))
    await unm_e.edit("```Unmuted this chat Successfully```")
    await sleep(2)
    await unm_e.delete()





# Regex-Ninja module by @Kandnub
regexNinja = False


@register(outgoing=True, pattern="^s/")
async def sedNinja(event):
    """For regex-ninja module, auto delete command starting with s/"""
    if regexNinja:
        await sleep(.5)
        await event.delete()


@register(outgoing=True, pattern="^.regexninja (on|off)$")
async def sedNinjaToggle(event):
    """ Enables or disables the regex ninja module. """
    global regexNinja
    if event.pattern_match.group(1) == "on":
        regexNinja = True
        await event.edit("`Successfully enabled ninja mode for Regexbot.`")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "off":
        regexNinja = False
        await event.edit("`Successfully disabled ninja mode for Regexbot.`")
        await sleep(1)
        await event.delete()


CMD_HELP.update({
    "chat":
    ".chatid\
\nUsage: Fetches the current chat's ID\
\n\n.userid\
\nUsage: Fetches the ID of the user in reply, if its a forwarded message, finds the ID for the source.\
\n\n.log\
\nUsage: Forwards the message you've replied to in your bot logs group.\
\n\n.kickme\
\nUsage: Leave from a targeted group.\
\n\n.unmutechat\
\nUsage: Unmutes a muted chat.\
\n\n.mutechat\
\nUsage: Allows you to mute any chat.\
\n\n.link <username/userid> : <optional text> (or) reply to someone's message with .link <optional text>\
\nUsage: Generate a permanent link to the user's profile with optional custom text.\
\n\n.regexninja on/off\
\nUsage: Globally enable/disables the regex ninja module.\
\nRegex Ninja module helps to delete the regex bot's triggering messages."
})
