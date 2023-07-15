"""
Cute Bot 2.0
Version 0.1
"""

import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        super().__init__(command_prefix='*', intents=intents, activity=discord.Game("Type *help for help"))
        self.coglist = ["cogs.textcommands"]

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Cute Bot is online " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        # uncomment below if using slash commands
        #synched = await self.tree.sync()
        #print(prfx + " Slash CMDs Synched " + Fore.YELLOW + str(len(synched)) + " Commands")

    async def setup_hook(self):
        for ext in self.coglist:
            await self.load_extension(ext)

client = Client()

with open("token.0", "r", encoding="utf-8") as f:
    TOKEN = f.read()

client.run(TOKEN)
