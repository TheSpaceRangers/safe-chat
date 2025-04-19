from discord import Interaction, app_commands

def channel_only(*channel_ids: int):
    def predicate(interaction: Interaction) -> bool:
        return interaction.channel.id in channel_ids
    return app_commands.check(predicate)