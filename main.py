# Quick and dirty roleplaying bot for discord
# Imports
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from cogs.dice_roller import get_dice_list, dice_roll, get_operation, proficiency_bonus, get_dice, get_max_side
from message_components import HelpComponent, RollComponent

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
    print(f"{interaction.user} run the 'help' command!")
    help_view = HelpComponent()
    await interaction.response.send_message(view=help_view, ephemeral=True)

# Dice roll related commands

# Listing out available dice
@bot.tree.command(name='dice_list', description='List available dice', guild=GUILD)
async def dice_list_out(interaction: discord.Interaction):
    print(f"{interaction.user} run the 'dice_list' command!")
    get_dice_list_result = get_dice_list()
    await interaction.response.send_message(f"List of available dice:\n {get_dice_list_result }", ephemeral=True)

@bot.tree.command(name='roll', description='A simple dice roll with optional proficiency modifiers (+, -)', guild=GUILD)
async def roll(interaction: discord.Interaction, dice:str, prof:str | None = None):
    print(f"{interaction.user} run the 'roll' command!")
    die = get_dice(dice)
    die_max = get_max_side(die)
    if die is None:
        await interaction.response.send_message("Invalid dice!", ephemeral=True)
        print(f"{interaction.user} used an invalid dice!")
        return

    dice_roll_result = dice_roll(die)
    nat_color = None
    if dice_roll_result == 1:
        nat_color = [209, 19, 19]
    if dice_roll_result == die_max:
        nat_color = [30, 212, 78]

    if prof is not None:
        print(f"{interaction.user} used a modifier!")
        operation_type = prof[0]
        chosen_operation = get_operation(operation_type)
        try:
            operation_value = int(prof[1:5])
            if operation_value is None:
                print(f"{interaction.user} used an invalid value!")
                await interaction.response.send_message("Invalid operation value!", ephemeral=True)
        except ValueError:
            print(f"{interaction.user} used an invalid value!")
            await interaction.response.send_message("Invalid operation value!", ephemeral=True)

        if chosen_operation is None:
            print(f"{interaction.user} used an invalid operation type!")
            await interaction.response.send_message("Invalid operation type!", ephemeral=True)
            return
        final_dice_roll_result = proficiency_bonus(chosen_operation, operation_value, dice_roll_result)
        prof = prof[0:5]
        final_dice_roll_result_string = f"{prof}={final_dice_roll_result}"
    else:
        print(f"{interaction.user} didn't use a modifier!")
        final_dice_roll_result = ""
        final_dice_roll_result_string = ""
    sidebar_color = nat_color
    print(dice_roll_result)
    print(final_dice_roll_result)

    roll_view = RollComponent(dice, dice_roll_result, interaction.user, final_dice_roll_result_string, sidebar_color)
    await interaction.response.send_message(view=roll_view)








# Running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)