import discord
import yaml
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
other_logs_channel_id = data["Channels"]["OTHER_LOGS_CHANNEL_ID"]

class RoleEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel = self.bot.get_channel(other_logs_channel_id)
        try:
            embed = discord.Embed(
                description=
                f"""
{role.mention} ({role.name})
""",
                color=discord.Color.from_str(embed_color))
            embed.set_author(name=f"Role Created", icon_url=role.guild.icon.url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Role: {role.id}")
            await channel.send(embed=embed)
            return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        channel = self.bot.get_channel(other_logs_channel_id)
        try:
            if before.name != after.name:
                embed = discord.Embed(
                    description=
                    f"""
**Before**
{before.name}

**After**
{after.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Role Name Updated", icon_url=before.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Role: {before.id}")
                await channel.send(embed=embed)
                return

            list1 = []
            list2 = []
            if before.permissions != after.permissions:
                diff = set(after.permissions).difference(set(before.permissions))
                for perm, value in diff:
                    if value == True:
                        list1.append(perm)
                    else:
                        list2.append(perm)
                added = ' \n➕ '.join(list1)
                removed = '\n➖ '.join(list2)
                if added == '':
                    embed = discord.Embed(
                        description=
                        f"""

**Removed**
➖ {removed}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"Role Permissions Updated", icon_url=before.guild.icon.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Role: {before.id}")
                    await channel.send(embed=embed)
                    return
                if removed == '':
                    embed = discord.Embed(
                        description=
                        f"""

**Added**
➖ {added}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"Role Permissions Updated", icon_url=before.guild.icon.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Role: {before.id}")
                    await channel.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(
                        description=
                        f"""

**Added**
➕ {added}

**Removed**
➖ {removed}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"Role Permissions Updated", icon_url=before.guild.icon.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Role: {before.id}")
                    await channel.send(embed=embed)
                    return
            if before.color != after.color:
                embed = discord.Embed(
                    description=
                    f"""
**Before**
{before.color}

**After**
{after.color}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Role Color Updated", icon_url=before.guild.icon.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Role: {before.id}")
                await channel.send(embed=embed)
                return
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel = self.bot.get_channel(other_logs_channel_id)
        try:
            embed = discord.Embed(
                description=
                f"""
{role.name}
""",
                color=discord.Color.from_str(embed_color))
            embed.set_author(name=f"Role Deleted", icon_url=role.guild.icon.url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Role: {role.id}")
            await channel.send(embed=embed)
            return
        except:
            pass

async def setup(bot):
    await bot.add_cog(RoleEventsCog(bot))