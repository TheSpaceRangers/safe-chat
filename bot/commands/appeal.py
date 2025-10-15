from os import getenv

from discord import Interaction, app_commands


MOD_APPEALS_CHANNEL_ID = int(getenv("DISCORD_APPEALS_CHANNEL_ID", "0"))


class Appeal(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="appeal",
            description="Contester une décision de modération"
        )

    @app_commands.command(
        name="submit",
        description="Soumettre une contestation de suppression"
    )
    async def submit(self, interaction: Interaction, message_link: str, justification: str):
        await interaction.response.send_message(
            "Votre demande a été envoyée à l'équipe de modération.",
            ephemeral=True
        )

        if MOD_APPEALS_CHANNEL_ID:
            channel = interaction.client.get_channel(MOD_APPEALS_CHANNEL_ID)
            if channel is not None:
                await channel.send(
                    f"[Appeal] De {interaction.user.mention}\nMessage: {message_link}\nJustification: {justification}"
                )

