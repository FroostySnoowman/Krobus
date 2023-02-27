import discord
import yaml
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
other_logs_channel_id = data["Channels"]["OTHER_LOGS_CHANNEL_ID"]

class VoiceEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = self.bot.get_channel(other_logs_channel_id)
        try:
            if after.channel and not before.channel:
                embed = discord.Embed(
                    description=
                    f"""
{after.channel.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Voice Channel Joined", icon_url=after.channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {after.channel.id} | Member: {member.id}")
                await channel.send(embed=embed)
                return
            if before.channel and not after.channel:
                embed = discord.Embed(
                    description=
                    f"""
{before.channel.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Voice Channel Left", icon_url=before.channel.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Channel: {before.channel.id} | Member: {member.id}")
                await channel.send(embed=embed)
                return
        except:
            pass

async def setup(bot):
    await bot.add_cog(VoiceEventsCog(bot))