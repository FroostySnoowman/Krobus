import discord
import yaml
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
dm_logs_channel_id = data["Channels"]["DM_LOGS_CHANNEL_ID"]
other_logs_channel_id = data["Channels"]["OTHER_LOGS_CHANNEL_ID"]

class MessageEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message: discord.Message):
        if not isinstance(message.channel, discord.DMChannel) or message.author.bot:
            return
        else:
            guild = self.bot.get_guild(guild_id)
            author = await guild.fetch_member(message.author.id)
            if not author:
                author = message.author

        content = message.clean_content

        embed = discord.Embed()
        embed.set_author(name="{} ({}#{})".format(author.display_name, author.name, author.discriminator),
                icon_url=author.display_avatar.url)
        embed.timestamp = message.created_at
        embed.set_footer(text='User ID: {}'.format(author.id))
        embed.color = author.color

        embed.add_field(name="Message", value=content[:1000] or "blank")
        if len(content[1000:]) > 0:
            embed.add_field(name="(Continued)", value=content[1000:])
        
        channel = self.bot.get_channel(dm_logs_channel_id)
        await channel.send(content=f"{message.author.id}", embed=embed)

        try:
            await message.add_reaction('📬')
        except discord.ext.commands.errors.CommandInvokeError:
            await message.channel.send('📬')

    @commands.Cog.listener('on_message_delete')
    async def onmessagedelete(self, message: discord.Message):
        if message.guild:
            if message.author.bot:
                return
            channel = self.bot.get_channel(other_logs_channel_id)
            try:
                if message.attachments:
                    embed = discord.Embed(
                        description=
                        f"""
**Message sent by {message.author.mention} deleted in {message.channel.mention}**
{message.content}

**Contained an image**
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"{message.author}", icon_url=message.author.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")
                    await channel.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(
                        description=
                        f"""
**Message sent by {message.author.mention} deleted in {message.channel.mention}**
{message.content}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"{message.author}", icon_url=message.author.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")
                    await channel.send(embed=embed)
                    return
            except:
                pass
        else:
            pass

    @commands.Cog.listener('on_message_edit')
    async def onmessage(self, before, after):
        if before.guild:
            if before.author.bot:
                return
            channel = self.bot.get_channel(other_logs_channel_id)
            try:
                if after.attachments:
                    if before.content == '':
                        embed = discord.Embed(
                            description=
                            f"""
**Message edited in {before.channel.mention}** [Jump To Message]({before.jump_url})

**After**
{after.content}

**Image**
{after.attachments[0].url}
""",
                            color=discord.Color.from_str(embed_color))
                        embed.set_author(name=f"{before.author}", icon_url=before.author.display_avatar.url)
                        embed.timestamp=datetime.now()
                        embed.set_footer(text=f"Author: {before.author.id} | Message ID: {before.id}")
                        await channel.send(embed=embed)
                        return
                    else:
                        embed = discord.Embed(
                            description=
                            f"""
**Message edited in {before.channel.mention}** [Jump To Message]({before.jump_url})

**Before**
{before.content}
**After**
{after.content}

**Image**
{after.attachments[0].url}
""",
                            color=discord.Color.from_str(embed_color))
                        embed.set_author(name=f"{before.author}", icon_url=before.author.display_avatar.url)
                        embed.timestamp=datetime.now()
                        embed.set_footer(text=f"Author: {before.author.id} | Message ID: {before.id}")
                        await channel.send(embed=embed)
                        return
                else:
                    embed = discord.Embed(
                        description=
                        f"""
**Message edited in {before.channel.mention}** [Jump To Message]({before.jump_url})

**Before**
{before.content}
**After**
{after.content}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"{before.author}", icon_url=before.author.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Author: {before.author.id} | Message ID: {before.id}")
                    await channel.send(embed=embed)
                    return
            except:
                pass
        else:
            pass

async def setup(bot):
    await bot.add_cog(MessageEventsCog(bot))