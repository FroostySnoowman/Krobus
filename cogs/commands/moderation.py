import discord
import aiosqlite
import asyncio
import yaml
import re
import datetime as DT
from discord import app_commands
from discord.ext import commands, tasks
from typing import Optional
from datetime import datetime, timedelta

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
muted_role_id = data["General"]["MUTED_ROLE_ID"]
moderation_channel_id = data["Channels"]["MOD_LOGS_CHANNEL_ID"]

class History(discord.ui.Select):
    def __init__(self, bot, member: discord.Member = None):
        self.bot = bot
        self.member = member
        options = [
            discord.SelectOption(label='Warns'),
            discord.SelectOption(label='Mutes'),
            discord.SelectOption(label='Kicks'),
            discord.SelectOption(label='Bans')
        ]
        super().__init__(placeholder='What logs would you like to view?', min_values=1, max_values=1, options=options, custom_id="moderation:1")

    async def callback(self, interaction: discord.Interaction):
        guild = self.bot.get_guild(guild_id)
        if self.values[0] == 'Warns':
            db = await aiosqlite.connect('database.db')
            member = guild.get_member(self.member.id)
            cursor = await db.execute('SELECT * FROM warns WHERE member_id=?', (member.id,))
            rows = await cursor.fetchall()
            await db.close()
            if rows == []:
                embed = discord.Embed(description=f"{member.mention} has no warns to view!", color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(title=f"Warns of {member}", color=discord.Color.from_str(embed_color))
                counter = 1
                for row in rows:
                    embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nModerator: {row[2]} \nTime Issued: <t:{row[3]}:F> \n")
                    counter += 1
            await interaction.response.edit_message(embed=embed)
            return
        if self.values[0] == 'Mutes':
            db = await aiosqlite.connect('database.db')
            member = guild.get_member(self.member.id)
            cursor = await db.execute('SELECT * FROM mutes WHERE member_id=?', (member.id,))
            rows = await cursor.fetchall()
            await db.close()
            if rows == []:
                embed = discord.Embed(description=f"{member.mention} has no mutes to view!", color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(title=f"Mutes of {member}", color=discord.Color.from_str(embed_color))
                counter = 1
                for row in rows:
                    if row[4] == 'null':
                        embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nMod: {row[2]} \nTime Issued: {row[3]} \nTime Expired: Permanent")
                    elif row[4] == 'expired':
                        embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nMod: {row[2]} \nTime Issued: {row[3]} \nTime Expired: Expired")
                    else:
                        a = int(row[4])
                        embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nMod: {row[2]} \nTime Issued: {row[3]} \nTime Expired: <t:{a}:t>")
                    counter += 1
            await interaction.response.edit_message(embed=embed)
            return
        if self.values[0] == 'Kicks':
            db = await aiosqlite.connect('database.db')
            member = guild.get_member(self.member.id)
            cursor = await db.execute('SELECT * FROM kicks WHERE member_id=?', (member.id,))
            rows = await cursor.fetchall()
            await db.close()
            if rows == []:
                embed = discord.Embed(description=f"{member.mention} has no kicks to view!", color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(title=f"Kicks of {member}", color=discord.Color.from_str(embed_color))
                counter = 1
                for row in rows:
                    embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nModerator: {row[2]} \nTime Issued: <t:{row[3]}:F> \n")
                    counter += 1
            await interaction.response.edit_message(embed=embed)
            return
        if self.values[0] == 'Bans':
            db = await aiosqlite.connect('database.db')
            member = guild.get_member(self.member.id)
            cursor = await db.execute('SELECT * FROM bans WHERE member_id=?', (member.id,))
            rows = await cursor.fetchall()
            await db.close()
            if rows == []:
                embed = discord.Embed(description=f"{member.mention} has no bans to view!", color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(
                    title=f"Bans of {member}", color=discord.Color.from_str(embed_color))
                counter = 1
                for row in rows:
                    if row[4] == 'null':
                        embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nMod: {row[2]} \nTime Issued: {row[3]} \nTime Expired: Permanent")
                    elif row[4] == 'expired':
                        embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nMod: {row[2]} \nTime Issued: {row[3]} \nTime Expired: Expired")
                    else:
                        a = int(row[4])
                        embed.add_field(name=f"#{counter}", value=f"Reason: {row[1]} \nMod: {row[2]} \nTime Issued: {row[3]} \nTime Expired: <t:{a}:t>")
                    counter += 1
            await interaction.response.edit_message(embed=embed)
            return

class HistoryView(discord.ui.View):
    def __init__(self, bot, member: discord.Member = None):
        super().__init__(timeout=None)
        self.add_item(History(bot, member))

class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def cog_load(self):
        self.muteLoop.start()
        self.banLoop.start()

    @tasks.loop(seconds = 5)
    async def muteLoop(self):
        guild = self.bot.get_guild(guild_id)
        moderation_channel = self.bot.get_channel(moderation_channel_id)
        muted_role = guild.get_role(muted_role_id)
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM mutes')
        a = await cursor.fetchall()
        for row in a:
            await asyncio.sleep(1)
            if row[4] == 'null':
                continue
            if row[4] == 'expired':
                continue
            if row[4] <= DT.datetime.now().timestamp():
                member = guild.get_member(row[0])
                cursor = await db.execute('UPDATE mutes SET time_expired=? WHERE time_expired=?', ('expired', row[0]))
                await member.remove_roles(muted_role)
                embed = discord.Embed(title="Member Unmuted", description=f"{member.mention} ({member.id}) was unmuted automatically as the time expired has passed.", color=discord.Color.from_str(embed_color))
                embed.timestamp = datetime.now()
                embed.set_author(name=member, icon_url=member.display_avatar.url)
                await moderation_channel.send(embed=embed)
        await db.commit()
        await db.close()

    @muteLoop.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds = 5)
    async def banLoop(self):
        guild = self.bot.get_guild(guild_id)
        moderation_channel = self.bot.get_channel(moderation_channel_id)
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM bans')
        a = await cursor.fetchall()
        for row in a:
            await asyncio.sleep(1)
            if row[4] == 'null':
                continue
            if row[4] == 'expired':
                continue
            if row[4] <= DT.datetime.now().timestamp():
                cursor = await db.execute('UPDATE mutes SET time_expired=? WHERE time_expired=?', ('expired', row[0]))
                member = discord.Object(id=row[0])
                await guild.unban(member)
                member = guild.get_member(row[0])
                embed = discord.Embed(title="Member Unbanned", description=f"{member.mention} ({member.id}) was unbanned automatically as the time expired has passed.", color=discord.Color.from_str(embed_color))
                embed.timestamp = datetime.now()
                embed.set_author(name=member, icon_url=member.display_avatar.url)
                await moderation_channel.send(embed=embed)
        await db.commit()
        await db.close()

    @banLoop.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="ban", description="Bans a member!")
    @app_commands.describe(member="Who do you want to ban?")
    @app_commands.describe(time="How long do you want to ban them for? Ex: 7d")
    @app_commands.describe(reason="What is the reason for this ban?")
    @app_commands.default_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, time: Optional[str], reason: str) -> None:
        db = await aiosqlite.connect('database.db')
        moderation_channel = self.bot.get_channel(moderation_channel_id)
        if time is None:
            try:
                embed = discord.Embed(title="Banned", description=f"You were banned from {interaction.guild.name} for **{reason}**! \n\nThis ban will not expire.", color=discord.Color.from_str(embed_color))
                await member.send(embed=embed)
                embed = discord.Embed(title="Member Banned", description=f"Successfully banned {member.mention} for **{reason}**! \n\nThis ban will not expire.", color=discord.Color.from_str(embed_color))
            except:
                embed = discord.Embed(title="Member Banned", description=f"Successfully banned {member.mention} for **{reason}**! \n\nThis ban will not expire. \n\nA PM was not sent to the member.", color=discord.Color.from_str(embed_color))
            await member.ban(reason=reason)
            await db.execute('INSERT INTO bans VALUES (?,?,?,?,?);', (member.id, reason, interaction.user.id, int(DT.datetime.now().timestamp()), 'null'))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                time_list = re.split('(\d+)',time)
                if time_list[2] == "s":
                    time_in_s = int(time_list[1])
                if time_list[2] == "m":
                    time_in_s = int(time_list[1]) * 60
                if time_list[2] == "h":
                    time_in_s = int(time_list[1]) * 60 * 60
                if time_list[2] == "d":
                    time_in_s = int(time_list[1]) * 60 * 60 * 24
                x = datetime.now() + timedelta(seconds=time_in_s)
                ts = int(x.timestamp())
                embed = discord.Embed(title="Member Banned", description=f"{member.mention} ({member.id}) was banned for **{reason}** by {interaction.user.mention} ({interaction.user.id})! \n\nThis ban will expire at <t:{ts}:F>!", color=discord.Color.from_str(embed_color))
                embed.timestamp = datetime.now()
                embed.set_author(name=member, icon_url=member.display_avatar.url)
                await moderation_channel.send(embed=embed)
                try:
                    embed = discord.Embed(title="Banned", description=f"You were banned from {interaction.guild.name} for **{reason}**! \n\nThis ban will expire at <t:{ts}:F>!", color=discord.Color.from_str(embed_color))
                    await member.send(embed=embed)
                    embed = discord.Embed(title="Member Banned", description=f"Successfully banned {member.mention} for **{reason}**! \n\nThis ban will expire at <t:{ts}:F>!", color=discord.Color.from_str(embed_color))
                except:
                    embed = discord.Embed(title="Member Banned", description=f"Successfully banned {member.mention} for **{reason}**! \n\nThis ban will expire at <t:{ts}:F>! \n\nA PM was not sent to the member.", color=discord.Color.from_str(embed_color))
                await member.ban(reason=reason)
                await db.execute('INSERT INTO bans VALUES (?,?,?,?,?);', (member.id, reason, interaction.user.id, int(DT.datetime.now().timestamp()), ts))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except IndexError:
                embed = discord.Embed(description=f"Failed to conver {time} to a valid time. The valid options are `s`, `m`, `h`, and `d`. Ex: 7d", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()
        
    @app_commands.command(name="kick", description="Kicks a member!")
    @app_commands.describe(member="Who do you want to kick?")
    @app_commands.describe(reason="What is the reason for this kick?")
    @app_commands.default_permissions(administrator=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str) -> None:
        db = await aiosqlite.connect('database.db')
        moderation_channel = self.bot.get_channel(moderation_channel_id)
        embed = discord.Embed(title="Member Kicked", description=f"{member.mention} ({member.id}) was kicked for **{reason}** by {interaction.user.mention} ({interaction.user.id})!", color=discord.Color.from_str(embed_color))
        embed.timestamp = datetime.now()
        embed.set_author(name=member, icon_url=member.display_avatar.url)
        await moderation_channel.send(embed=embed)
        embed = discord.Embed(description=f"Sucessfully kicked {member.mention} for **{reason}**!", color=discord.Color.from_str(embed_color))
        try:
            embed = discord.Embed(title="Kicked", description=f"You were kicked from {interaction.guild.name} for **{reason}**!", color=discord.Color.from_str(embed_color))
            await member.send(embed=embed)
        except:
            embed = discord.Embed(description=f"Sucessfully kicked {member.mention} for **{reason}**! \n\nA PM was not sent to the member.", color=discord.Color.from_str(embed_color))
        await member.kick(reason=reason)
        await db.execute('INSERT INTO kicks VALUES (?,?,?,?);', (member.id, reason, interaction.user.id, int(DT.datetime.now().timestamp())))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="mute", description="Mutes a member!")
    @app_commands.describe(member="Who do you want to mute?")
    @app_commands.describe(time="How long do you want to mute them for? Ex: 7d")
    @app_commands.describe(reason="What is the reason for this mute?")
    @app_commands.default_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, time: Optional[str], reason: str) -> None:
        db = await aiosqlite.connect('database.db')
        moderation_channel = self.bot.get_channel(moderation_channel_id)
        muted_role = interaction.guild.get_role(muted_role_id)
        if time is None:
            await member.add_roles(muted_role)
            try:
                embed = discord.Embed(title="Muted", description=f"You were muted in {interaction.guild.name} for **{reason}**! \n\nThis mute will not expire.", color=discord.Color.from_str(embed_color))
                await member.send(embed=embed)
                embed = discord.Embed(title="Member Muted", description=f"Successfully muted {member.mention} for **{reason}**! \n\nThis mute will not expire.", color=discord.Color.from_str(embed_color))
            except:
                embed = discord.Embed(title="Member Muted", description=f"Successfully muted {member.mention} for **{reason}**! \n\nThis mute will not expire. \n\nA PM was not sent to the member.", color=discord.Color.from_str(embed_color))
            await db.execute('INSERT INTO mutes VALUES (?,?,?,?,?);', (member.id, reason, interaction.user.id, int(DT.datetime.now().timestamp()), 'null'))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                time_list = re.split('(\d+)',time)
                if time_list[2] == "s":
                    time_in_s = int(time_list[1])
                if time_list[2] == "m":
                    time_in_s = int(time_list[1]) * 60
                if time_list[2] == "h":
                    time_in_s = int(time_list[1]) * 60 * 60
                if time_list[2] == "d":
                    time_in_s = int(time_list[1]) * 60 * 60 * 24
                x = datetime.now() + timedelta(seconds=time_in_s)
                ts = int(x.timestamp())
                await member.add_roles(muted_role)
                embed = discord.Embed(title="Member Muted", description=f"{member.mention} ({member.id}) was muted for **{reason}** by {interaction.user.mention} ({interaction.user.id})! \n\nThis mute will expire at <t:{ts}:F>!", color=discord.Color.from_str(embed_color))
                embed.timestamp = datetime.now()
                embed.set_author(name=member, icon_url=member.display_avatar.url)
                await moderation_channel.send(embed=embed)
                try:
                    embed = discord.Embed(title="Muted", description=f"You were muted in {interaction.guild.name} for **{reason}**! \n\nThis mute will expire at <t:{ts}:F>!", color=discord.Color.from_str(embed_color))
                    await member.send(embed=embed)
                    embed = discord.Embed(title="Member Muted", description=f"Successfully muted {member.mention} for **{reason}**! \n\nThis mute will expire at <t:{ts}:F>!", color=discord.Color.from_str(embed_color))
                except:
                    embed = discord.Embed(title="Member Muted", description=f"Successfully muted {member.mention} for **{reason}**! \n\nThis mute will expire at <t:{ts}:F>! \n\nA PM was not sent to the member.", color=discord.Color.from_str(embed_color))
                await db.execute('INSERT INTO mutes VALUES (?,?,?,?,?);', (member.id, reason, interaction.user.id, int(DT.datetime.now().timestamp()), ts))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except IndexError:
                embed = discord.Embed(description=f"Failed to conver {time} to a valid time. The valid options are `s`, `m`, `h`, and `d`. Ex: 7d", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="warn", description="Warns a member!")
    @app_commands.describe(member="Who do you want to warn?")
    @app_commands.describe(reason="What is the reason for this warn?")
    @app_commands.default_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str) -> None:
        db = await aiosqlite.connect('database.db')
        moderation_channel = self.bot.get_channel(moderation_channel_id)
        embed = discord.Embed(title="Member Warned", description=f"{member.mention} ({member.id}) was warned for **{reason}** by {interaction.user.mention} ({interaction.user.id})!", color=discord.Color.from_str(embed_color))
        embed.timestamp = datetime.now()
        embed.set_author(name=member, icon_url=member.display_avatar.url)
        await moderation_channel.send(embed=embed)
        try:
            embed = discord.Embed(title="Warn", description=f"You were warned in {interaction.guild.name} for **{reason}**!", color=discord.Color.from_str(embed_color))
            await member.send(embed=embed)
            embed = discord.Embed(description=f"Successfully warned {member.mention} for **{reason}**!", color=discord.Color.from_str(embed_color))
        except:
            embed = discord.Embed(description=f"Successfully warned {member.mention} for **{reason}**! \n\nA PM was not sent to the member.", color=discord.Color.from_str(embed_color))
        await db.execute('INSERT INTO warns VALUES (?,?,?,?);', (member.id, reason, interaction.user.id, int(DT.datetime.now().timestamp())))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="purge", description="Purges/deletes messages!")
    @app_commands.describe(limit="What's the limit of messages you want to delete?")
    @app_commands.default_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction, limit: int) -> None:
        await interaction.response.send_message("Clearing...", ephemeral=True)
        await interaction.channel.purge(limit=limit)
        await interaction.edit_original_response(content="Cleared!")

    @app_commands.command(name="history", description="Views the history of a user!")
    @app_commands.describe(member="Who's history do you want to view?")
    @app_commands.default_permissions(administrator=True)
    async def history(self, interaction: discord.Interaction, member: discord.Member) -> None:
        bot = self.bot
        view = HistoryView(bot, member)
        embed = discord.Embed(
            title=f"History of {member}", description="Choose the type of history you would like to view!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationCog(bot), guilds=[discord.Object(id=guild_id)])