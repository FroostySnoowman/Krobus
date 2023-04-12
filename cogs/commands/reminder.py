import discord
import datetime as DT
import aiosqlite
import asyncio
import yaml
import re
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
dm_logs_channel_id = data["Channels"]["DM_LOGS_CHANNEL_ID"]

class ReminderCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def cog_load(self):
        self.reminderLoop.start()

    @tasks.loop(seconds = 5)
    async def reminderLoop(self):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM reminders')
        a = await cursor.fetchall()
        for b in a:
            await asyncio.sleep(1)
            if b[2] <= DT.datetime.now().timestamp():
                await db.execute('DELETE FROM reminders WHERE time_expired=?', (b[2], ))
                channel = self.bot.get_channel(b[3])
                message = channel.get_partial_message(b[4])
                embed = discord.Embed(description=f"Your reminder for **{b[1]}** just ended!", color=discord.Color.from_str(embed_color))
                try:
                    await message.reply(content=f"<@{b[0]}>", embed=embed)
                except:
                    await channel.send(content=f"<@{b[0]}>", embed=embed)
        await db.commit()
        await db.close()

    @reminderLoop.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="remindme", description="Reminds you of something!")
    @app_commands.describe(reminder="What should I remind you of?")
    @app_commands.describe(time="When should I remind you? Ex: 7d")
    @app_commands.default_permissions(administrator=True)
    async def dm(self, interaction: discord.Interaction, reminder: str, time: str) -> None:
        db = await aiosqlite.connect('database.db')
        a = DT.datetime.now().timestamp()
        b = int(a)
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
            timestamp = DT.datetime.now().timestamp()
            x = datetime.now() + timedelta(seconds=time_in_s)
            timestamp = x.timestamp()
            a = int(timestamp)
            b = int(a)
            
            embed = discord.Embed(description=f"I'll remind you of **{reminder}** at <t:{b}:F>! (<t:{b}:R>)", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed)
            msg = await interaction.original_response()
            await db.execute('INSERT INTO reminders VALUES (?,?,?,?,?);', (interaction.user.id, f'{reminder}', timestamp, interaction.channel.id, msg.id))
        except:
            embed = discord.Embed(description="Please retry this command again! There seems to be an error with the time. \nIn the time, assure that you only have `s`, `m`, `h`, or `d` once.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(ReminderCog(bot), guilds=[discord.Object(id=guild_id)])