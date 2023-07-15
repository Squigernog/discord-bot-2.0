# Cog for bot text commands

import discord
from discord.ext import commands
from discord import app_commands
import random

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

        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(textcommands(client))