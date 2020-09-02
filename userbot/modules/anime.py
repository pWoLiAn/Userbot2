# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import html
import json
import textwrap
from io import BytesIO, StringIO
from urllib.parse import quote as urlencode

import aiohttp
import bs4
import pendulum
import requests


from telethon.errors.rpcerrorlist import FilePartsInvalidError
from telethon.tl.types import (DocumentAttributeAnimated,
                               DocumentAttributeFilename, MessageMediaDocument)
from telethon.utils import is_image, is_video

from userbot import CMD_HELP
from userbot.events import register



# Anime Helper


def replace_text(text):
    return text.replace(
        '"',
        "").replace(
        "\\r",
        "").replace(
            "\\n",
            "").replace(
                "\\",
        "")


@register(outgoing=True, pattern=r"^\.a(kaizoku|kayo) ?(.*)")
async def site_search(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(2).strip()
    site = event.pattern_match.group(1).strip()
    if search_query:
        pass
    elif message:
        search_query = message.text.strip()
    else:
        await event.edit("`I can't search void LoL`")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        if search_result:
            result = f"<b><a href='{search_url.replace(' ','%20')}'>Search results</a> for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n"
            for entry in search_result:
                post_link = entry.a["href"]
                post_name = html.escape(entry.text.strip())
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
            await event.edit(result, parse_mode="HTML")
        else:
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"
            await event.edit(result, parse_mode="HTML")

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        if search_result:
            result = f"<b><a href='{search_url.replace(' ','%20')}'>Search results</a> for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"
        await event.edit(result, parse_mode="HTML")




@register(outgoing=True, pattern=r"^\.wait")
async def whatanime(e):
    media = e.media
    if not media:
        r = await e.get_reply_message()
        media = getattr(r, "media", None)
    if not media:
        await e.edit("`Media required`")
        return
    ig = is_gif(media) or is_video(media)
    if not is_image(media) and not ig:
        await e.edit("`Media must be an image or gif or video`")
        return
    filename = "file.jpg"
    if not ig and isinstance(media, MessageMediaDocument):
        attribs = media.document.attributes
        for i in attribs:
            if isinstance(i, DocumentAttributeFilename):
                filename = i.file_name
                break
    await e.edit("`Downloading image..`")
    content = await e.client.download_media(media, bytes, thumb=-1 if ig else None)
    await e.edit("`Searching for result..`")
    file = memory_file(filename, content)
    async with aiohttp.ClientSession() as session:
        url = "https://trace.moe/api/search"
        async with session.post(url, data={"image": file}) as raw_resp0:
            resp0 = await raw_resp0.text()
        js0 = json.loads(resp0)["docs"]
        if not js0:
            await e.edit("`No results found.`")
            return
        js0 = js0[0]
        text = f'<b>{html.escape(js0["title_romaji"])}'
        if js0["title_native"]:
            text += f' ({html.escape(js0["title_native"])})'
        text += "</b>\n"
        if js0["episode"]:
            text += f'<b>Episode:</b> {html.escape(str(js0["episode"]))}\n'
        percent = round(js0["similarity"] * 100, 2)
        text += f"<b>Similarity:</b> {percent}%\n"
        dt = pendulum.from_timestamp(js0["at"])
        text += f"<b>At:</b> {html.escape(dt.to_time_string())}"
        await e.edit(text, parse_mode="html")
        dt0 = pendulum.from_timestamp(js0["from"])
        dt1 = pendulum.from_timestamp(js0["to"])
        ctext = (
            f"{html.escape(dt0.to_time_string())} - {html.escape(dt1.to_time_string())}"
        )
        url = (
            "https://trace.moe/preview.php"
            f'?anilist_id={urlencode(str(js0["anilist_id"]))}'
            f'&file={urlencode(js0["filename"])}'
            f'&t={urlencode(str(js0["at"]))}'
            f'&token={urlencode(js0["tokenthumb"])}'
        )
        async with session.get(url) as raw_resp1:
            file = memory_file("preview.mp4", await raw_resp1.read())
        try:
            await e.reply(ctext, file=file, parse_mode="html")
        except FilePartsInvalidError:
            await e.reply("`Cannot send preview.`")


def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode()
    file = BytesIO() if bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file


def is_gif(file):
    # ngl this should be fixed, telethon.utils.is_gif but working
    # lazy to go to github and make an issue kek
    if not is_video(file):
        return False
    if DocumentAttributeAnimated() not in getattr(
            file, "document", file).attributes:
        return False
    return True


CMD_HELP.update({
    "anime":
    "`.akaizoku` or `.akayo` <anime name>\
    \nUsage: Returns with the Anime Download link.\
    \n\n`.wait` Reply with media.\
    \nUsage: Find anime from media file."
})
