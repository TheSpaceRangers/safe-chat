from os import getenv

from discord import Interaction, app_commands

from aiohttp import ClientSession

from utils import channel_only

API_URL = getenv("MODERATION_API_URL", "http://localhost:8000/api/v1")

class Api(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="api",
            description="Api description"
        )

    @app_commands.command(
        name="version",
        description="Affiche la version de l'api de modération"
    )
    @channel_only(int(getenv("DISCORD_COMMAND_CHANNEL_ID", "0")))
    async def version(self, interaction: Interaction):
        async with ClientSession() as session:
            async with session.get(f"{API_URL}/version") as response:
                data = await response.json()
                await interaction.response.send_message(f"Version de l'API : {data.get('version')}")