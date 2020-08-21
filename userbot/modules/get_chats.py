import os
from asyncio import sleep



from userbot.modules.sql_helper.users_sql import get_user_com_chats
from userbot.events import register
from telethon.utils import get_display_name
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.errors.rpcerrorlist import UnauthorizedError, BadRequestError


@register(pattern=".getchats(?: |$)(.*)", outgoing=True)
async def who(event):
    replied_user = await get_user(event)
    if not replied_user:
        await event.edit("I share no common chats with the void.")
        return
    common_list = get_user_com_chats(replied_user)
    if not common_list:
        await event.edit("No common chats with this user!")
        return
    name = replied_user.user.first_name
    text = f"<b>Common chats with {name}</b>\n"
    for chat in common_list:
        try:
            chat_name = get_display_name(chat)
            await sleep(0.3)
            text += f"• <code>{chat_name}</code>\n"
        except BadRequestError:
            pass
        except UnauthorizedError:
            pass


    if len(text) < 4096:
        await event.edit(text, parse_mode="HTML")
    else:
        await event.edit('Too many groups.take txt.')
        with open("common_chats.txt", 'w+') as f:
            f.write(text)

        await event.client.send_file(event.chat_id,
                                         "common_chats.txt",
                                         reply_to=event.id)
        os.remove("common_chats.txt")


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user
