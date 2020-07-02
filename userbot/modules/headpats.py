# thenku phoenix-chan for url
import os
import json
import aiohttp
import asyncio
import random
from urllib.parse import quote as urlencode
from telethon import events
from userbot.events import register
from userbot import CMD_HELP

_pats = []

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

    
    CMD_HELP.update({
    'pat':
    '.pat\
\nUsage: sends random pat gifs.'
})
