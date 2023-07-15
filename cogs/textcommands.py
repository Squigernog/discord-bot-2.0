# Cog for bot text commands

import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

eightball_responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
                       "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                       "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

class textcommands(commands.Cog):

    # Init cog
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="pfp", description="Display the profile picture of a user")
    async def pfp(self, ctx, member:discord.Member=None):
        # Check if member mentioned
        if member == None:
            member = ctx.message.author
        embed = discord.Embed()
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="8ball", description="Consult the 8 ball on your present or future")
    async def eightball(self, ctx):
        # Check if question asked
        if (ctx.message.content == self.client.command_prefix + "8ball"):
            await ctx.reply("Please ask me a question")
        else:
            selection = random.randint(0, 20)
            await ctx.reply(eightball_responses[selection])

    @commands.command(name="joint", description="Pass a user the virtual joint. If no user mentioned, send to random user.")
    async def joint(self, ctx, member:discord.Member=None):
        # grab file
        filePath = "./images/virtual_joint.gif"

        # check if member mentioned
        if member == None:
            # Verify random user is not bot
            while True:
                member = random.choice(ctx.message.channel.guild.members)
                if not member.bot:
                    break

        member = "<@" + str(member.id) + ">"
        await ctx.send(content=member, file=discord.File(filePath))

    @commands.command(name="bonk", description="Bonk a user")
    async def bonk(self, ctx, member:discord.Member=None):
        # grab file
        fileNumber = random.randint(1, 7)
        filePath = "./images/bonk/" + str(fileNumber) + ".gif"

        # check if member mentioned
        if member == None:
            member = ctx.message.author
            await ctx.reply("You bonked yourself!", file=discord.File(filePath))
        else:
            await ctx.send("You bonked " + str(member), file=discord.File(filePath))

    @commands.command(name="roll", description="Roll x amount of y sided dice. Format: xdy")
    async def roll(self, ctx, roll : str):
        num, type = roll.split('d')
        type = int(type)
        result = 0

        for i in range(0, int(num)):
            result += random.randint(1, type)
        
        await ctx.reply(str(result))

    @commands.command(name="soy", description="Depict your enemies with a soyjak. Select between numbers 1 and 42.")
    async def soy(self, ctx, number : str = None):
        # Verify selection
        if(number == None): # random file if no selection
            number = str(random.randint(1, 42))
        
        filePath = "./images/soy/still/" + number + ".png"

        try:
            # Check for and get replied message
            reference = ctx.message.reference
            if(reference != None):
                msg = await ctx.fetch_message(reference.message_id)

                img = Image.open(filePath)
                font = ImageFont.truetype("arial.ttf", 48)

                soyjak = Image.open(filePath)
                speechBubble = Image.open("./images/soy/speech bubble.png")

                # Concat selected soyjak & speech bubble
                img = concatImages(speechBubble, soyjak)
                draw = ImageDraw.Draw(img)

                # Calculate text position
                W = img.width / 5
                H = img.height / 5

                draw.text((W, H), msg.content, (255,255,255), font=font)
                bytes = BytesIO()
                img.save(bytes, format="PNG")
                bytes.seek(0)

                await ctx.send(file=discord.File(bytes, filename="img.png"))
            else:
                await ctx.send("soy", file=discord.File(filePath))
        except FileNotFoundError:
            await ctx.send("Invalid selection")

def concatImages(im1, im2, resample=Image.BICUBIC, resize_big_image=True, color=(54,57,62)):
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

async def setup(client:commands.Bot) -> None:
    await client.add_cog(textcommands(client))
