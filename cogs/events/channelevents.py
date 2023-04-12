import discord
import yaml
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
other_logs_channel_id = data["Channels"]["OTHER_LOGS_CHANNEL_ID"]

class ChannelEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        logschannel = self.bot.get_channel(other_logs_channel_id)
        try:
            if isinstance(channel, discord.CategoryChannel):
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Category Channel Created", icon_url=channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                await logschannel.send(embed=embed)
                return
            if isinstance(channel, discord.VoiceChannel):
                embed = discord.Embed(
                    description=
                    f"""
{channel.mention}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Voice Channel Created", icon_url=channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                await logschannel.send(embed=embed)
                return
            if isinstance(channel, discord.TextChannel):
                embed = discord.Embed(
                    description=
                    f"""
{channel.mention}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Text Channel Created", icon_url=channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                await logschannel.send(embed=embed)
                return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        logschannel = self.bot.get_channel(other_logs_channel_id)
        try:
            if isinstance(channel, discord.CategoryChannel):
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Category Channel Deleted", icon_url=channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                await logschannel.send(embed=embed)
                return
            if isinstance(channel, discord.VoiceChannel):
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Voice Channel Deleted", icon_url=channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                await logschannel.send(embed=embed)
                return
            if isinstance(channel, discord.TextChannel):
                embed = discord.Embed(
                    description=
                    f"""
{channel.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Text Channel Deleted", icon_url=channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {channel.id}")
                await logschannel.send(embed=embed)
                return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        channel = self.bot.get_channel(other_logs_channel_id)
        try:
            if before.name != after.name:
                embed = discord.Embed(
                    description=
                    f"""

**{before.mention} name updated!**

**Before**:
{before.name}

**After**:
{after.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"{before.guild.name}", icon_url=before.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {before.id}")
                await channel.send(embed=embed)
        except:
            pass

async def setup(bot):
    await bot.add_cog(ChannelEventsCog(bot))