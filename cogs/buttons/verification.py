import discord
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
verified_role_id = data["Verification"]["VERIFIED_ROLE_ID"]
muted_role_id = data["General"]["MUTED_ROLE_ID"]

class VerificationButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='✅', label='Verify', style=discord.ButtonStyle.green, custom_id='verification:1')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        verified = interaction.guild.get_role(verified_role_id)
        muted = interaction.guild.get_role(muted_role_id)
        if muted in interaction.user.roles:
            embed = discord.Embed(description="Don't try to get around a mute!", color=discord.Color.red())
        elif verified in interaction.user.roles:
            embed = discord.Embed(description="You're already verified!", color=discord.Color.red())
        else:
            await interaction.user.add_roles(verified)
            embed = discord.Embed(description="You've successfully been verified!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

class VerificationButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(VerificationButton())

async def setup(bot):
    await bot.add_cog(VerificationButtonCog(bot), guilds=[discord.Object(id=guild_id)])