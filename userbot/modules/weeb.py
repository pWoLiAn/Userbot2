
import nekos
import os
import json
import aiohttp
import asyncio
import random
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from urllib.parse import quote as urlencode
from telethon import events
from userbot.events import register
from userbot import CMD_HELP, bot
from asyncio import sleep


_pats = []
jikan = Jikan()



@register(outgoing=True, pattern=r"^.anime (.*)")
async def asearch(event):
    msg = event.pattern_match.group(1)
    res = ""
    try:
        res = jikan.search("anime", msg)
    except APIException:
        await event.edit("Error connecting to the API. Please try again!")
        return ""
    try:
        res = res.get("results")[0].get("mal_id") # Grab first result
    except APIException:
        await event.edit("Error connecting to the API. Please try again!")
        return ""
    if res:
        anime = jikan.anime(res)
        title = anime.get("title")
        japanese = anime.get("title_japanese")
        type = anime.get("type")
        duration = anime.get("duration")
        synopsis = anime.get("synopsis")
        source = anime.get("source")
        status = anime.get("status")
        episodes = anime.get("episodes")
        score = anime.get("score")
        rating = anime.get("rating")
        genre_lst = anime.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        studios = ""
        studio_lst = anime.get("studios")
        for studio in studio_lst:
            studios += studio.get("name") + ", "
        studios = studios[:-2]
        duration = anime.get("duration")
        premiered = anime.get("premiered")
        image_url = anime.get("image_url")
        url = anime.get("url")
        trailer = anime.get("trailer_url")
    else:
        await event.edit("No results found!")
        return
    rep = f"<b>{title} ({japanese})</b>\n"
    rep += f"<b>Type:</b> <code>{type}</code>\n"
    rep += f"<b>Source:</b> <code>{source}</code>\n"
    rep += f"<b>Status:</b> <code>{status}</code>\n"
    rep += f"<b>Genres:</b> <code>{genres}</code>\n"
    rep += f"<b>Episodes:</b> <code>{episodes}</code>\n"
    rep += f"<b>Duration:</b> <code>{duration}</code>\n"
    rep += f"<b>Score:</b> <code>{score}</code>\n"
    rep += f"<b>Studio(s):</b> <code>{studios}</code>\n"
    rep += f"<b>Premiered:</b> <code>{premiered}</code>\n"
    rep += f"<b>Rating:</b> <code>{rating}</code>\n\n"
    rep += f"<a href='{image_url}'>\u200c</a>"
    rep += f"<i>{synopsis}</i>\n"
    await event.edit(rep, parse_mode='html')
    

@register(outgoing=True, pattern=r"^.pat(?: |$)")
async def pat(e):
    global _pats
    
    
    url = 'https://headp.at/js/pats.json'
    if not _pats:
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as raw_resp:
                resp = await raw_resp.text()
        _pats = json.loads(resp)
    pats = _pats
    
    pats = [i for i in pats if os.path.splitext(i)[1] == '.gif']
    
    pat = random.choice(pats)
    link = f'https://headp.at/pats/{urlencode(pat)}'
    
    await asyncio.wait([
        e.respond(file=link, reply_to=e.reply_to_msg_id),
        e.delete()
    ])


@register(outgoing=True, pattern="^\.pgif(?: |$)(.*)")
async def pussyg(e):
    await e.edit("`Finding some pussy gifs...`")
    await sleep(2)
    target = 'pussy'
    await bot.send_file(e.chat_id, nekos.img(target), reply_to=e.reply_to_msg_id)
    await e.delete()
   

@register(outgoing=True, pattern="^\.pjpg(?: |$)(.*)")
async def pussyp(e):
    await e.edit("`Finding some pussy pics...`")
    await sleep(2)
    target = 'pussy_jpg'
    await bot.send_file(e.chat_id, nekos.img(target), reply_to=e.reply_to_msg_id)
    await e.delete()


@register(outgoing=True, pattern="^\.cum(?: |$)(.*)")
async def cum(e):
    await e.edit("`Finding some cum gifs...`")
    await sleep(2)
    target = 'cum'
    await bot.send_file(e.chat_id, nekos.img(target), reply_to=e.reply_to_msg_id)
    await e.delete()


CMD_HELP.update({
    'weeb':
    "`.pgif`"
    "\nUsage: Get pussy gif.\n"
    "`.pjpg`"
    "\nUsage: Get pussy image.\n"
    "`.pat`"
    "\nUsage: Get random pat gif.\n"
    "`.cum`"
    "\nUsage: Get random cum gif.\n"
    "`.anime`"
    "\nUsage: Get details about given anime."
})
