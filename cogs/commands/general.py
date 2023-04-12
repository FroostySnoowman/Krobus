import discord
import time
from discord import app_commands
from discord.ext import commands

class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Sends the ping of the bot!")
    @app_commands.default_permissions(administrator=True)
    async def ping(self, interaction: discord.Interaction) -> None:
        start = time.perf_counter()
        await interaction.response.send_message("Pinging...", ephemeral=True)
        end = time.perf_counter()
        duration = (end - start) * 1000
        await interaction.edit_original_response(content='Pong! {:.2f}ms'.format(duration))

    @app_commands.command(name="latency", description="Sends the latency of the bot!")
    @app_commands.default_permissions(administrator=True)
    async def latency(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('{0} ms'.format(round(self.bot.latency, 1)), ephemeral=True)

async def setup(bot):
    await bot.add_cog(GeneralCog(bot))