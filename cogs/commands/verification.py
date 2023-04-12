import discord
import yaml
from discord import app_commands
from discord.ext import commands
from cogs.buttons.verification import VerificationButton

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class VerificationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="verification", description="Sends the verification panel!")
    @app_commands.default_permissions(administrator=True)
    async def verification(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="Rules and Verification", description="""
**Be Respectful**
This should go without saying, but please be kind and respectful of each other. We are all here to enjoy and create content for Stardew Valley.

**No harassment**
There will be no harassment of any form on this server. This is a space for cooperation and collaboration. Harassment will not be tolerated.

A particular note on this topic, in the modding community there is a very blurry line between mod-creator and mod-enjoyer. It's easy to get wrapped up in talking about content we feel passionate about. 
There's a chance that creators not within the conversation, who are also in the community to enjoy Stardew Valley, will see what you're saying about the content or creator. Please keep this in mind as we continue to enjoy content-making.

**No NSFW content**
We are a 13+ server, therefore NSFW is not allowed.

**Server Links**
Please do not link to other discords or social media groups outside our #Friends Servers channel and the main discord.  If you have something you feel belongs in our Friends channel please reach out to a moderator.

**Media, Art and Mods**
All media, art, and mods shared or posted should adhere to the other rules of this server. 

**Other Advertisements**
If you have an advertisement that fits within the rules of the server, but does not fit into the categories of “server link, media, arts or mods” please reach out to someone on the moderation team and we'll find an appropriate home for your links. All such requests should come from the developer/creator of the product being advertised.

**Tone**
Reading tone can be difficult. It can be conveyed with choice of words, modulation and inflection of voice, and physical expressions among others.  On the internet we have only our choice of words which add an extra barrier to effective communication. 

Tone indicators are a way to incorporate some of that missing physical and auditory information. For your reference, here's a list of commonly accepted indicators you could use at the end of a sentence to convey the meaning you intend. 

/j = joking
/hj = half joking
/srs = serious
/s = sarcastic
/lh = light hearted
/nm = not mad
/gen = genuinely
/neg = negative connotation
/pos = positive connotation
/t = teasing
/ly = lyrics

**Critiquing**
Sometimes people will share work looking for constructive critiques or help with a specific problem. Sometimes people will be sharing a cool thing they did. Please be respectful of what the creator is comfortable with, and work within the bounds of what they ask for.

Please keep in mind this is a hobby and we are all creating content for different, equally valid reasons. 

To help navigate this, and the different types of critiques, here's some critique categories creators could use as a guideline when asking for advice. If no category is given please lean more toward gentle on the spectrum than harsh.

Gentle Critique - be very kind when providing help, focusing on small changes with a heavy focus on what is working.
General Critique - a comprehensive critique covering what is both working and not working while keeping a pleasant tone in mind.
Harsh Critique - everything is fair game, as long it's respectful.
""", color=discord.Color.from_str(embed_color))
        embed2 = discord.Embed(description="""
**A note on the housekeeping boards**
Shadow Crafters are able to post on some of the housekeeping boards, and everyone verified can post on introductions.
We'd like to keep these channels tidy, so information is findable later so these channels will be periodically purged. 
Feel free to discuss and be excited in channels like General!

**Voice Chat Rules**
Please be conscious of tone and feelings in VC, just as you would elsewhere at Krobus. 
If you have noise going on in the background, are away from keyboard, or are talking to someone out of VC (ie family, on a phone call, etc), please mute yourself. 
While game-streaming is not limited to the movies and video game voice channel, please be conscientious that people are trying to work on mods in the mod-making channel. Likewise, if there's a multi-player game going on please be conscientious that they're using the voice channel to play their game.
Do not talk during a movie, please keep yourself on mute throughout the duration of the movie. If you would like to have a voice conversation, please use a different VC channel.

If you have any questions or concerns please reach out to one of the Shadow Sentinels (our moderator team). 

Click the button below to become verified and gain access to the rest of the server!
""", color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embeds=[embed, embed2], view=VerificationButton())
        embed = discord.Embed(description="Sent!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(VerificationCog(bot), guilds=[discord.Object(id=guild_id)])