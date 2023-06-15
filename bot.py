import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SPINNING_WHEEL_CHANNEL = os.getenv("CHANNEL_ID")
SPINNING_WHEEL_USER = os.getenv("USER_ID")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await bot.tree.sync()


bot.run(TOKEN)
