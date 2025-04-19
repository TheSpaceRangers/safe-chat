from os import getenv

from dotenv import load_dotenv

from discord import Intents, Interaction, Message, app_commands
from discord.ext.commands import Bot

from commands import Api, Topics

from utils import moderate_content, replace_with_placeholder

load_dotenv()

bot = Bot(
    command_prefix="!",
    intents=Intents.all()
)

@bot.event
async def on_ready():
    bot.tree.add_command(Api())
    bot.tree.add_command(Topics())
    await bot.tree.sync()
    await bot.get_channel(int(getenv("DISCORD_CHANNEL_ID", "0"))).send(f"Bot connecté : {bot.user}")

@bot.tree.error
async def on_app_command_error(interaction: Interaction, error: Exception):
    if isinstance(error, app_commands.errors.CheckFailure):
        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"❌ Cette commande n'est pas autorisée dans ce channel.",
                ephemeral=True
            )
        return
    raise error

@bot.event
async def on_message(message: Message):
    if message.author.bot:
        return

    result = await moderate_content(message.content)

    if result.get("action") == "delete":
        await replace_with_placeholder(message, result.get("reason"))

bot.run(getenv('DISCORD_TOKEN'))