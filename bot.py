import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SPINNING_WHEEL_CHANNEL = os.getenv("CHANNEL_ID")
SPINNING_WHEEL_USER = os.getenv("USER_ID")

intents = discord.Intents.default()
intents.message_content = True

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

        if discord.utils.get(message.reactions, emoji="⬆️"):
            reaction = discord.utils.get(message.reactions, emoji="⬆️")
            reaction_count = reaction.count
        else:
            reaction_count = 0

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


@bot.tree.command(
    name="generate", description="Get the top 10 challenges and 5 extra substitutes."
)
async def send_challenges(interaction: discord.Interaction):
    
    if interaction.user.id != SPINNING_WHEEL_USER:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        return
    
    count = 1
    challenges = await sort_challenges()

    channel_id = str(SPINNING_WHEEL_CHANNEL)
    channel = bot.get_channel(int(channel_id))

    output = "# Top 10 Challenges:\n"

    for challenge in challenges[:5]:
        challenge_output = f"**{count})** {challenge.get('challenge')} - **{challenge.get('reactions')}** ⬆️ - by <@{challenge.get('user')}> -> {challenge.get('link')}\n"
        output += challenge_output
        count += 1

    # split the top 10 into 2 messages because of 2000 character limit
    output2 = ""

    for challenge in challenges[6:11]:
        challenge_output = f"**{count})** {challenge.get('challenge')} - **{challenge.get('reactions')}** ⬆️ - by <@{challenge.get('user')}> -> {challenge.get('link')}\n"
        output2 += challenge_output
        count += 1

    subs_output = "# Next 5 Substitute Challenges:\n"

    for challenge in challenges[11:16]:
        challenge_subs = f"**{count})** {challenge.get('challenge')} - **{challenge.get('reactions')}** ⬆️ - by {challenge.get('username')} -> {challenge.get('link')}\n"
        subs_output += challenge_subs
        count += 1

    await interaction.response.send_message(output)
    await channel.send(output2)
    await channel.send(subs_output)

    return


bot.run(TOKEN)
