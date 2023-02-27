import discord
import yaml
from discord import app_commands
from discord.ext import commands
from cogs.buttons.verification import VerificationButton

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class VerificationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="verification", description="Sends the verification panel!")
    @app_commands.default_permissions(administrator=True)
    async def suggest(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="Verification", description="Click the button below to become verified and gain access to the rest of the server!", color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embed=embed, view=VerificationButton())
        embed = discord.Embed(description="Sent!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(VerificationCog(bot), guilds=[discord.Object(id=guild_id)])