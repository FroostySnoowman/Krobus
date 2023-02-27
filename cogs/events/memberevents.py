import discord
import asyncio
import yaml
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
member_logs_channel_id = data["Channels"]["MEMBER_LOGS_CHANNEL_ID"]

class MemberEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.bot:
            return
        channel = self.bot.get_channel(member_logs_channel_id)
        try:
            if before.name != after.name:
                embed = discord.Embed(
                    description=
                    f"""
**{before.mention} name changed

**Before**
{before.name}
**After**
{after.name}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"{before}", icon_url=before.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {before.id}")
                await channel.send(embed=embed)
        except:
            pass
        try:
            if before.nick != after.nick:
                embed = discord.Embed(
                    description=
                    f"""
**{before.mention} nickname changed**

**Before**
{before.nick}
**After**
{after.nick}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"{before}", icon_url=before.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {before.id}")
                await channel.send(embed=embed)
        except:
            pass
        try:
            if before.roles != after.roles:
                before_set = set(before.roles)
                after_set = set(after.roles)
                added_roles = after_set - before_set
                removed_roles = before_set - after_set
                added = ' \n➕ '.join(role.mention for role in added_roles)
                removed = ' \n➖ '.join(role.mention for role in removed_roles)

                if added == '':
                    embed = discord.Embed(
                        description=
                        f"""

**{before.mention} roles removed!**

➖ {removed}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"{before}", icon_url=before.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Member: {before.id}")
                    await channel.send(embed=embed)
                    return
                if removed == '':
                    embed = discord.Embed(
                        description=
                        f"""

**{before.mention} roles added!**

➕ {added}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"{before}", icon_url=before.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Member: {before.id}")
                    await channel.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(
                        description=
                        f"""

**{before.mention} roles changed!**

➕ {added}
➖ {removed}
""",
                        color=discord.Color.from_str(embed_color))
                    embed.set_author(name=f"{before}", icon_url=before.display_avatar.url)
                    embed.timestamp=datetime.now()
                    embed.set_footer(text=f"Member: {before.id}")
                    await channel.send(embed=embed)
                    return
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        try:
            channel = self.bot.get_channel(member_logs_channel_id)
            created = int(member.created_at.timestamp())
            embed = discord.Embed(
                description=
                f"""
{member.mention} {member}

**Account Created**
<t:{created}:R>
""",
                color=discord.Color.from_str(embed_color))
            embed.set_author(name=f"Member Joined", icon_url=member.display_avatar.url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Member: {member.id}")
            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return
        await asyncio.sleep(5)
        channel = self.bot.get_channel(member_logs_channel_id)
        try:
            entries = [
                entry
                async for entry in member.guild.audit_logs(limit=1)
                if entry.action in (discord.AuditLogAction.kick, discord.AuditLogAction.ban)
                and entry.target.id == member.id
            ]
            if entries == []:
                role = ', '.join(x.name for x in member.roles) 
                embed = discord.Embed(
                    description=
                    f"""
{member.mention} {member}

**Roles**
{role}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Member Left", icon_url=member.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {member.id}")
                await channel.send(embed=embed)
                return
            if entries[0].action == discord.AuditLogAction.kick:
                role = ', '.join(x.name for x in member.roles) 
                embed = discord.Embed(
                    description=
                    f"""
{member.mention} ({member}) was kicked by {entries[0].user}

**Roles**
{role}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Member Kicked", icon_url=member.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {member.id}")
                await channel.send(embed=embed)
                return
            if entries[0].action == discord.AuditLogAction.ban:
                role = ', '.join(x.name for x in member.roles) 
                embed = discord.Embed(
                    description=
                    f"""
{member.mention} ({member}) was banned by {entries[0].user}

**Roles**
{role}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_author(name=f"Member Banned", icon_url=member.display_avatar.url)
                embed.timestamp=datetime.now()
                embed.set_footer(text=f"Member: {member.id}")
                await channel.send(embed=embed)
                return
        except:
            pass

async def setup(bot):
    await bot.add_cog(MemberEventsCog(bot))