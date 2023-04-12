import discord
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
red_color_role_id = data["Roles"]["RED_COLOR_ROLE_ID"]
blue_color_role_id = data["Roles"]["BLUE_COLOR_ROLE_ID"]
yellow_color_role_id = data["Roles"]["YELLOW_COLOR_ROLE_ID"]
purple_color_role_id = data["Roles"]["PURPLE_COLOR_ROLE_ID"]
pink_color_role_id = data["Roles"]["PINK_COLOR_ROLE_ID"]
sheher_pronoun_role_id = data["Roles"]["SHEHER_PRONOUN_ROLE_ID"]
hehim_pronount_role_id = data["Roles"]["HEHIM_PRONOUN_ROLE_ID"]
theythem_pronoun_role_id = data["Roles"]["THEYTHEM_PRONOUN_ROLE_ID"]
any_pronoun_role_id = data["Roles"]["ANY_PRONOUN_ROLE_ID"]
ask_pronoun_role_id = data["Roles"]["ASK_PRONOUN_ROLE_ID"]

class RoleColorButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='🔴', label='Red', style=discord.ButtonStyle.gray, custom_id='color:1')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        red = interaction.guild.get_role(red_color_role_id)
        blue = interaction.guild.get_role(blue_color_role_id)
        yellow = interaction.guild.get_role(yellow_color_role_id)
        purple = interaction.guild.get_role(purple_color_role_id)
        pink = interaction.guild.get_role(pink_color_role_id)
        if red in interaction.user.roles:
            await interaction.user.remove_roles(red)
            embed = discord.Embed(description=f"Successfully removed the {red.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            if blue in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {blue.mention} role to choose a new one!", color=discord.Color.red())
            elif yellow in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {yellow.mention} role to choose a new one!", color=discord.Color.red())
            elif purple in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {purple.mention} role to choose a new one!", color=discord.Color.red())
            elif pink in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {pink.mention} role to choose a new one!", color=discord.Color.red())
            else:
                await interaction.user.add_roles(red)
                embed = discord.Embed(description=f"Successfully added the {red.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='🔵', label='Blue', style=discord.ButtonStyle.gray, custom_id='color:2')
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        red = interaction.guild.get_role(red_color_role_id)
        blue = interaction.guild.get_role(blue_color_role_id)
        yellow = interaction.guild.get_role(yellow_color_role_id)
        purple = interaction.guild.get_role(purple_color_role_id)
        pink = interaction.guild.get_role(pink_color_role_id)
        if blue in interaction.user.roles:
            await interaction.user.remove_roles(blue)
            embed = discord.Embed(description=f"Successfully removed the {blue.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            if red in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {red.mention} role to choose a new one!", color=discord.Color.red())
            elif yellow in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {yellow.mention} role to choose a new one!", color=discord.Color.red())
            elif purple in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {purple.mention} role to choose a new one!", color=discord.Color.red())
            elif pink in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {pink.mention} role to choose a new one!", color=discord.Color.red())
            else:
                await interaction.user.add_roles(blue)
                embed = discord.Embed(description=f"Successfully added the {blue.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='🟡', label='Yellow', style=discord.ButtonStyle.gray, custom_id='color:3')
    async def yellow(self, interaction: discord.Interaction, button: discord.ui.Button):
        red = interaction.guild.get_role(red_color_role_id)
        blue = interaction.guild.get_role(blue_color_role_id)
        yellow = interaction.guild.get_role(yellow_color_role_id)
        purple = interaction.guild.get_role(purple_color_role_id)
        pink = interaction.guild.get_role(pink_color_role_id)
        if yellow in interaction.user.roles:
            await interaction.user.remove_roles(yellow)
            embed = discord.Embed(description=f"Successfully removed the {yellow.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            if red in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {red.mention} role to choose a new one!", color=discord.Color.red())
            elif blue in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {blue.mention} role to choose a new one!", color=discord.Color.red())
            elif purple in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {purple.mention} role to choose a new one!", color=discord.Color.red())
            elif pink in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {pink.mention} role to choose a new one!", color=discord.Color.red())
            else:
                await interaction.user.add_roles(yellow)
                embed = discord.Embed(description=f"Successfully added the {yellow.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='🟣', label='Purple', style=discord.ButtonStyle.gray, custom_id='color:4')
    async def purple(self, interaction: discord.Interaction, button: discord.ui.Button):
        red = interaction.guild.get_role(red_color_role_id)
        blue = interaction.guild.get_role(blue_color_role_id)
        yellow = interaction.guild.get_role(yellow_color_role_id)
        purple = interaction.guild.get_role(purple_color_role_id)
        pink = interaction.guild.get_role(pink_color_role_id)
        if purple in interaction.user.roles:
            await interaction.user.remove_roles(purple)
            embed = discord.Embed(description=f"Successfully removed the {purple.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            if red in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {red.mention} role to choose a new one!", color=discord.Color.red())
            elif blue in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {blue.mention} role to choose a new one!", color=discord.Color.red())
            elif yellow in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {yellow.mention} role to choose a new one!", color=discord.Color.red())
            elif pink in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {pink.mention} role to choose a new one!", color=discord.Color.red())
            else:
                await interaction.user.add_roles(purple)
                embed = discord.Embed(description=f"Successfully added the {purple.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='⚪', label='Pink', style=discord.ButtonStyle.gray, custom_id='color:5')
    async def pink(self, interaction: discord.Interaction, button: discord.ui.Button):
        red = interaction.guild.get_role(red_color_role_id)
        blue = interaction.guild.get_role(blue_color_role_id)
        yellow = interaction.guild.get_role(yellow_color_role_id)
        purple = interaction.guild.get_role(purple_color_role_id)
        pink = interaction.guild.get_role(pink_color_role_id)
        if pink in interaction.user.roles:
            await interaction.user.remove_roles(pink)
            embed = discord.Embed(description=f"Successfully removed the {pink.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            if red in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {red.mention} role to choose a new one!", color=discord.Color.red())
            elif blue in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {blue.mention} role to choose a new one!", color=discord.Color.red())
            elif yellow in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {yellow.mention} role to choose a new one!", color=discord.Color.red())
            elif purple in interaction.user.roles:
                embed = discord.Embed(description=f"You already have a color role assigned! Remove the {purple.mention} role to choose a new one!", color=discord.Color.red())
            else:
                await interaction.user.add_roles(pink)
                embed = discord.Embed(description=f"Successfully added the {pink.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='❌', label='Remove All', style=discord.ButtonStyle.gray, custom_id='color:6')
    async def pink(self, interaction: discord.Interaction, button: discord.ui.Button):
        red = interaction.guild.get_role(red_color_role_id)
        blue = interaction.guild.get_role(blue_color_role_id)
        yellow = interaction.guild.get_role(yellow_color_role_id)
        purple = interaction.guild.get_role(purple_color_role_id)
        pink = interaction.guild.get_role(pink_color_role_id)
        if red in interaction.user.roles:
            await interaction.user.remove_roles(red)
        if blue in interaction.user.roles:
            await interaction.user.remove_roles(blue)
        if yellow in interaction.user.roles:
            await interaction.user.remove_roles(yellow)
        if purple in interaction.user.roles:
            await interaction.user.remove_roles(purple)
        if pink in interaction.user.roles:
            await interaction.user.remove_roles(pink)
        embed = discord.Embed(description=f"Successfully removed all your color roles!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

class PronounRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='📘', label='She/Her', style=discord.ButtonStyle.gray, custom_id='pronouns:1')
    async def sheher(self, interaction: discord.Interaction, button: discord.ui.Button):
        sheher = interaction.guild.get_role(sheher_pronoun_role_id)
        if sheher in interaction.user.roles:
            await interaction.user.remove_roles(sheher)
            embed = discord.Embed(description=f"Successfully removed the {sheher.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            await interaction.user.add_roles(sheher)
            embed = discord.Embed(description=f"Successfully added the {sheher.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='📕', label='He/Him', style=discord.ButtonStyle.gray, custom_id='pronouns:2')
    async def hehim(self, interaction: discord.Interaction, button: discord.ui.Button):
        hehim = interaction.guild.get_role(hehim_pronount_role_id)
        if hehim in interaction.user.roles:
            await interaction.user.remove_roles(hehim)
            embed = discord.Embed(description=f"Successfully removed the {hehim.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            await interaction.user.add_roles(hehim)
            embed = discord.Embed(description=f"Successfully added the {hehim.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='📗', label='They/Them', style=discord.ButtonStyle.gray, custom_id='pronouns:3')
    async def theythem(self, interaction: discord.Interaction, button: discord.ui.Button):
        theythem = interaction.guild.get_role(theythem_pronoun_role_id)
        if theythem in interaction.user.roles:
            await interaction.user.remove_roles(theythem)
            embed = discord.Embed(description=f"Successfully removed the {theythem.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            await interaction.user.add_roles(theythem)
            embed = discord.Embed(description=f"Successfully added the {theythem.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='📙', label='Any', style=discord.ButtonStyle.gray, custom_id='pronouns:4')
    async def any(self, interaction: discord.Interaction, button: discord.ui.Button):
        any = interaction.guild.get_role(any_pronoun_role_id)
        if any in interaction.user.roles:
            await interaction.user.remove_roles(any)
            embed = discord.Embed(description=f"Successfully removed the {any.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            await interaction.user.add_roles(any)
            embed = discord.Embed(description=f"Successfully added the {any.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='📙', label='Ask Me', style=discord.ButtonStyle.gray, custom_id='pronouns:5')
    async def askme(self, interaction: discord.Interaction, button: discord.ui.Button):
        ask = interaction.guild.get_role(ask_pronoun_role_id)
        if ask in interaction.user.roles:
            await interaction.user.remove_roles(ask)
            embed = discord.Embed(description=f"Successfully removed the {ask.mention} role!", color=discord.Color.from_str(embed_color))
        else:
            await interaction.user.add_roles(ask)
            embed = discord.Embed(description=f"Successfully added the {ask.mention} role!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='❌', label='Remove All', style=discord.ButtonStyle.gray, custom_id='pronouns:6')
    async def askme(self, interaction: discord.Interaction, button: discord.ui.Button):
        sheher = interaction.guild.get_role(sheher_pronoun_role_id)
        hehim = interaction.guild.get_role(hehim_pronount_role_id)
        theythem = interaction.guild.get_role(theythem_pronoun_role_id)
        any = interaction.guild.get_role(any_pronoun_role_id)
        ask = interaction.guild.get_role(ask_pronoun_role_id)
        if sheher in interaction.user.roles:
            await interaction.user.remove_roles(sheher)
        if hehim in interaction.user.roles:
            await interaction.user.remove_roles(hehim)
        if theythem in interaction.user.roles:
            await interaction.user.remove_roles(theythem)
        if any in interaction.user.roles:
            await interaction.user.remove_roles(any)
        if ask in interaction.user.roles:
            await interaction.user.remove_roles(ask)
        embed = discord.Embed(description=f"Successfully removed all your pronoun roles!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

class RolesButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(RoleColorButtons())
        self.bot.add_view(PronounRoles())

async def setup(bot):
    await bot.add_cog(RolesButtonCog(bot), guilds=[discord.Object(id=guild_id)])