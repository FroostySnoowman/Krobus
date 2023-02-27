import discord
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
dm_logs_channel_id = data["Channels"]["DM_LOGS_CHANNEL_ID"]

class DmCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="dm", description="Sends a user a DM!")
    @app_commands.describe(member="Who would you like to DM?")
    @app_commands.describe(message="What message would you like to DM?")
    @app_commands.default_permissions(administrator=True)
    async def dm(self, interaction: discord.Interaction, member: discord.Member, message: str) -> None:
        if interaction.channel.id != dm_logs_channel_id:
            await interaction.response.send_message(f'You must be in the <#{dm_logs_channel_id}> channel!', ephemeral=True)
        else:
            try:
                author = interaction.user
                embed = discord.Embed()
                embed.set_author(name="Message", icon_url=interaction.channel.guild.icon)
                embed.color = author.color
                embed.add_field(name=f"Message from Krobus Moderation", value=message[:1000] or "blank", inline=False)
                if len(message) > 1000:
                    embed.add_field(name="(Continued)", value=message[1000:], inline=False)
                await member.send(embed=embed)

                author = interaction.user
                embed = discord.Embed()
                embed.set_author(name="DM Message", icon_url=interaction.channel.guild.icon)
                embed.color = author.color
                embed.add_field(name="Message:", value=message[:1000] or "blank", inline=False)
                if len(message) > 1000:
                    embed.add_field(name="(Continued)", value=message[1000:], inline=False)
                embed.add_field(name="To:", value=f"<@{member.id}> ({member.id})", inline=False)
                embed.add_field(name="From:", value=f"<@{author.id}> ({author.id})", inline=False)
                await interaction.response.send_message('Sent the following message:', embed=embed)
            except:
                await interaction.response.send_message("I cannot send that user a message! Please ask them to open their PMs!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DmCog(bot), guilds=[discord.Object(id=guild_id)])