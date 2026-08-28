# Quick and dirty roleplaying bot for discord
# Imports
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from cogs.dice_roller import dice_list, get_dice_list, dice_roll, advanced_dice_roll

# Loading bot token and guild id
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
# noinspection PyTypeChecker
GUILD_ID = int(os.getenv("GUILD_ID")) #converting guild id to int
GUILD = discord.Object(id=GUILD_ID)

# Setting bot intents (aka permissions)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot class, command sync and startup message
class QnDRPbot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync(guild=GUILD)
        print("Commands synced!")
    async def on_ready(self):
        print(f"Bot online as {bot.user.name}, ready to go!")

# Old command bot prefix, even though we don't use old prefixes,
# this is required for the code to function
# DO NOT touch this unless you want to break stuff
bot = QnDRPbot(command_prefix='!', intents=intents)

# General bot commands

# Ping "/" command for debugging
@bot.tree.command(name='ping', description='Ping the bot', guild=GUILD)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Help command with a list of functions
@bot.tree.command(name='help', description='List of functions and commands', guild=GUILD)
async def help_list(interaction: discord.Interaction):
    await interaction.response.send_message("List of available commands... not done yet tho o(╥﹏╥)o", ephemeral=True)

# Dice roll related commands

# Listing out available dice
@bot.tree.command(name='dice_list', description='List available dice', guild=GUILD)
async def dice_list_out(interaction: discord.Interaction):
    print(f"{interaction.user} run the 'dice_list' command!")
    get_dice_list_result = get_dice_list()
    await interaction.response.send_message(f"List of available dice:\n {get_dice_list_result }", ephemeral=True)

# Performing a simple dice roll with a single die
@bot.tree.command(name='roll', description='a simple dice roll', guild=GUILD)
async def roll(interaction: discord.Interaction, dice:str):
    print(f"{interaction.user} run the 'roll' command!")
    for die in dice_list:
        if die.name == dice:
            dice_roll_result = dice_roll(die)
            break
    else:
        await interaction.response.send_message("Invalid dice!", ephemeral=True)
        return
    await interaction.response.send_message(f"{interaction.user.mention} using {dice}\n rolled a {dice_roll_result}!")

# Performing an advance dice roll
@bot.tree.command(name='rollplus', description='an advanced dice roll', guild=GUILD)
async def roll_plus(interaction: discord.Interaction, expression:str):
    print(f"{interaction.user} run the 'rollplus' command!")
    # result = advanced_dice_roll(expression)
    await interaction.response.send_message(f"not done yet o(╥﹏╥)o")


# Running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)