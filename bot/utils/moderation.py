from os import getenv

from aiohttp import ClientSession

from discord import Message
from discord.utils import get

API_URL = getenv("MODERATION_API_URL", "http://localhost:8000/api/v1")

async def moderate_content(content: str) -> dict:
    async with ClientSession() as session:
        try:
            async with session.post(f"{API_URL}/moderate", json={ "content": content }) as response:
                return await response.json()
        except Exception as e:
            print(e)
            return {}

async def replace_with_placeholder(message: Message, reason: str):
    channel = message.channel
    try:
        await message.delete()
        webhooks = await channel.webhooks()
        webhook = get(webhooks, name="mod-placeholder")
        if webhook is None:
            webhook = await channel.create_webhook(name="mod-placeholder")

        await webhook.send(
            content="*Message supprimé par SafeChat*",
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url
        )
    except Exception as e:
        print(e)
    else:
        try:
            await message.author.send(f"🚫 Ton message a été supprimé : {reason}")
        except Exception as e:
            print(e)
