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


async def get_challenges():
    challenges = []

    channel_id = str(SPINNING_WHEEL_CHANNEL)
    channel = bot.get_channel(int(channel_id))

    async for message in channel.history():
        if len(message.content) < 125:
            text = message.content
        else:
            text = message.content[:125] + "..."

        stripped_text = text.replace("\n", "")

        reaction = discord.utils.get(message.reactions, emoji="⬆️")
        reaction_count = reaction.count
        user_id = message.author.id
        username = message.author.name
        message_url = message.jump_url

        challenges.append(
            {
                "challenge": stripped_text,
                "reactions": reaction_count,
                "user": user_id,
                "username": username,
                "link": message_url,
            }
        )

    return challenges


async def sort_challenges():
    challenges = await get_challenges()

    sorted_challenges = sorted(challenges, key=lambda d: d["reactions"], reverse=True)

    return sorted_challenges


bot.run(TOKEN)
