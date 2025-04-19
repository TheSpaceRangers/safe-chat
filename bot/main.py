from os import getenv
from dotenv import load_dotenv

from discord import Intents
from discord.ext.commands import Bot

load_dotenv()

bot = Bot(
    command_prefix="!",
    intents=Intents.all()
)

@bot.event
async def on_ready():
    await (bot.get_channel(getenv("DISCORD_CHANNEL_ID", "0"))
           .send("Bot démarré avec succès ✅"))

bot.run(getenv('DISCORD_TOKEN'))