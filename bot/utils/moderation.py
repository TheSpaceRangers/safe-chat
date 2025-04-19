from os import getenv

from aiohttp import ClientSession

from discord import Message, Embed, Color
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

        embed = Embed(
            title="*Message supprimé par SafeChat*",
            color=0x95A5A6,
            timestamp=message.created_at
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url
        )
        embed.set_footer(text="SafeChat", icon_url=message.guild.me.display_avatar.url)

        await webhook.send(
            embed=embed,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url
        )
    except Exception as e:
        print(e)
    else:
        await notify_user_deleted(message, reason)

async def notify_user_deleted(message: Message, reason: str):
    embed = Embed(
        title="🚫 Message supprimé",
        description=f"**Raison:** {reason}",
        color=Color.red()
    )
    embed.set_footer(text="SafeChat", icon_url=message.guild.me.display_avatar.url)

    try:
        await message.author.send(embed=embed)
    except Exception as e:
        print("Erreur DM:", e)