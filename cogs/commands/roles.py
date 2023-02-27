import discord
import yaml
from discord import app_commands
from discord.ext import commands
from cogs.buttons.roles import RoleColorButtons, PronounRoles

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="roles", description="Sends the roles panel!")
    @app_commands.default_permissions(administrator=True)
    async def roles(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="Roles", description="Assign or remove color roles by clicking the buttons below", color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embed=embed, view=RoleColorButtons())
        embed = discord.Embed(description="Assign or remove pronoun roles by clicking the buttons below", color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embed=embed, view=PronounRoles())
        embed = discord.Embed(description="Sent!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(RolesCog(bot), guilds=[discord.Object(id=guild_id)])