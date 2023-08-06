# Cog for bot text commands

import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw
import textwrap
from io import BytesIO
import requests

eightball_responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
                       "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                       "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

class textcommands(commands.Cog):

    # Init cog
    def __init__(self, client: commands.Bot):
        self.client = client

    #-------------------------- PFP Command ------------------------#
    @commands.command(name="pfp", description="Display the profile picture of a user")
    async def pfp(self, ctx, member:discord.Member=None):
        # Check if member mentioned
        if member == None:
            member = ctx.message.author
        embed = discord.Embed()
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    #-------------------------- 8ball Command ------------------------#
    @commands.command(name="8ball", description="Consult the 8 ball on your present or future")
    async def eightball(self, ctx):
        # Check if question asked
        if (ctx.message.content == self.client.command_prefix + "8ball"):
            await ctx.reply("Please ask me a question")
        else:
            selection = random.randint(0, 20)
            await ctx.reply(eightball_responses[selection])

    #-------------------------- Joint Command ------------------------#
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
    
    #-------------------------- Is Gay Command ------------------------#
    @commands.command(name="isgay", description="Determines who in the server is gay")
    async def isGay(self, ctx):
        member = ""
        while True:
            member = random.choice(ctx.message.channel.guild.members)
            if not member.bot:
                break

        message = "<@" + str(member.id) + "> is gay"

        await ctx.send(content=message)

    #-------------------------- Bonk Command ------------------------#
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

    #-------------------------- Roll Command ------------------------#
    @commands.command(name="roll", description="Roll x amount of y sided dice. Format: xdy")
    async def roll(self, ctx, roll : str):
        num, type = roll.split('d')
        type = int(type)
        result = 0

        for i in range(0, int(num)):
            result += random.randint(1, type)
        
        await ctx.reply(str(result))

    #-------------------------- Soy Command ------------------------#
    @commands.command(name="soy", description="Depict your enemies with a soyjak. Select between numbers 1 and 42. Reply to a message when using command to add text or iamge.")
    async def soy(self, ctx, number : str = None):
        # Verify selection
        if(number == None): # random file if no selection
            number = str(random.randint(1, 42))
        
        filePath = "./images/soy/still/" + number + ".png"

        try:
            # Check for and get replied message
            reference = ctx.message.reference
            if(reference != None):
                # Get referenced message
                msg = await ctx.fetch_message(reference.message_id)
                
                # Get font
                font = ImageFont.truetype("arial.ttf", 60)

                # Grab images
                soyjak = Image.open(filePath)
                speechBubble = Image.open("./images/soy/speech bubble.png")

                # Get center point of speech bubble
                W = speechBubble.width / 2
                H = speechBubble.height / 2

                # Concat selected soyjak & speech bubble
                img = concatImages(speechBubble, soyjak)
                draw = ImageDraw.Draw(img)
                
                # Check for attachment
                if(len(msg.attachments) != 0):
                    if(msg.attachments[0].content_type in ('image/jpeg', 'image/jpg', 'image/png', 'image/webp')):
                        # Resize and add to image
                        ref_img = msg.attachments[0]
                        with Image.open(requests.get(ref_img.url, stream=True).raw) as im:
                            ref_img_resize = resizeImage(im, speechBubble.width, speechBubble.height)
                            """w = int(speechBubble.width * 0.7)
                            h = int(speechBubble.height * 0.7)
                            ref_img_resize = im.resize([w, h])"""
                                
                            # Calculate image offset
                            x_offset = ref_img_resize.width / 2
                            y_offset = ref_img_resize.height / 2
                                
                            img.paste(ref_img_resize, (int(W - x_offset), int(H - y_offset)))
                    #elif(msg.attachments[0].content_type in ('image/gif')):
                        
                else:
                    # New line ever 24 characters
                    lines = textwrap.wrap(msg.content, width=24)
                    y_text = H
                    for line in lines:
                            draw.text((W, y_text), line, (255,255,255), font=font, align="center", anchor="mm")
                            y_text += 50
                    
                bytes = BytesIO()
                img.save(bytes, format="PNG")
                bytes.seek(0)

                await ctx.send(file=discord.File(bytes, filename="img.png"))
            # Send only soyjak if no referenced message
            else:
                await ctx.send("", file=discord.File(filePath))
        # If selected value does not exist
        except FileNotFoundError:
            await ctx.send("Invalid selection")

def concatImages(im1, im2):
    """
    Vertically concatenate two images. im1 on top and im2 on bottom.
    """
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def resizeImage(img:Image.Image, speech_w:int, speech_h:int):
    """
    Resize image with relation to the speech bubble's size
    If image is square, resize to 70% size of the speech bubble
    If width or height is larger that the other measurement, resize larger measurement to 70%
      of speech bubble size, then find the aspect ratio of image to set up a ratio equation to 
      find the other value.
    Ex.: if w < h, then x/(speech_h * 0.7) = W/H, where x is the resized width and W and H are
      the original values of the image
    """
    ref_img = img
    if (ref_img.width == ref_img.height):
        w = int(speech_w * 0.7)
        h = int(speech_h * 0.7)
        ref_img = ref_img.resize([w, h])
    elif (ref_img.width < ref_img.height):
        h = int(speech_h * 0.7)
        w = int(h * (ref_img.width / ref_img.height))
        ref_img = ref_img.resize([w, h])
    else:
        w = int(speech_w * 0.7)
        h = int(w * (ref_img.height / ref_img.width))
        ref_img = ref_img.resize([w, h])

    return ref_img

async def setup(client:commands.Bot) -> None:
    await client.add_cog(textcommands(client))
