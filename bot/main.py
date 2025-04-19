from discord import Intents
from discord.ext.commands import Bot

bot = Bot(
    command_prefix="!",
    intents=Intents.all()
)

@bot.event
async def on_ready():
    await (bot.get_channel(1362693353669529722)
           .send("Bot démarré avec succès ✅"))

bot.run("MTM2MjkyMTUyNzc0OTc3MTQwNA.GYpA8L.ztMp_cD6wvg6rpnmL7GxMdWYLALV8wz7OdSYjA")