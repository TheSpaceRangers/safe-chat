from os import getenv

from discord import Interaction, app_commands

from aiohttp import ClientSession

from utils import channel_only

API_URL = getenv("MODERATION_API_URL", "http://localhost:8000/api/v1")

class Topics(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="topics",
            description="Gérer ou afficher les sujets interdits"
        )

    @app_commands.command(
        name="list",
        description="Affiche la liste des sujets interdits"
    )
    @channel_only(int(getenv("DISCORD_COMMAND_CHANNEL_ID", "0")))
    async def list(self, interaction: Interaction):
        async with ClientSession() as session:
            async with session.get(f"{API_URL}/rule") as response:
                data = await response.json()
        md = "**Sujets interdits :**\n" + "\n".join(f"- {t}" for t in data["topics"])
        await interaction.response.send_message(md, ephemeral=True)

    @app_commands.command(
        name="add",
        description="Ajouter un sujet interdit"
    )
    @app_commands.describe(topic="Sujet à interdire")
    @channel_only(int(getenv("DISCORD_COMMAND_CHANNEL_ID", "0")))
    async def add(self, interaction: Interaction, topic: str):
        async with ClientSession() as session:
            async with session.post(f"{API_URL}/rule", json={"topic": topic}) as resp:
                data = await resp.json()
        md = "**Sujets interdits mis à jour :**\n" + "\n".join(f"- {t}" for t in data["topics"])
        await interaction.response.send_message(md, ephemeral=True)

    @app_commands.command(
        name="remove",
        description="Supprimer un sujet interdit"
    )
    @app_commands.describe(topic="Sujet à ne plus interdire")
    @channel_only(int(getenv("DISCORD_COMMAND_CHANNEL_ID", "0")))
    async def remove(self, interaction: Interaction, topic: str):
        async with ClientSession() as session:
            async with session.delete(f"{API_URL}/rule", json={"topic": topic}) as resp:
                data = await resp.json()
        md = "**Sujets interdits mis à jour :**\n" + "\n".join(f"- {t}" for t in data["topics"])
        await interaction.response.send_message(md, ephemeral=True)