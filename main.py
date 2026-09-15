# Quick and dirty roleplaying bot for discord
# Imports
import sys

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from cogs.dice_roller import (
    get_dice_list,
    dice_roll,
    get_operation,
    proficiency_bonus,
    get_dice,
    get_max_side,
    dice_validation_check,
    times_to_roll_validation_check,
    proficiency_validation_check,
    onNat_sidebar_color,
    multiple_dice_rolls,
)

from cogs.coin_flipper import (
    coinflip
)

from message_components import (
    HelpComponent,
    RollComponent,
    RollMultipleComponent,
    Roll2D6Component,
)

# Loading bot token and guild id
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
# noinspection PyTypeChecker
GUILD_ID = int(os.getenv("GUILD_ID")) #converting guild id to int
GUILD = discord.Object(id=GUILD_ID)

# Logging
# Discord.py logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Bot logging
bot_logger = logging.getLogger("Bot")
bot_file_handler = logging.FileHandler(filename='botlog.log', encoding='utf-8', mode='w')
bot_console_handler = logging.StreamHandler(sys.stdout)

bot_formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] | %(message)s')
bot_file_handler.setFormatter(bot_formatter)
bot_console_handler.setFormatter(bot_formatter)

bot_logger.addHandler(bot_file_handler)
bot_logger.addHandler(bot_console_handler)

# Checking if the debug mode is on
is_debug_mode_on = int(os.getenv("DEBUG_MODE"))
if is_debug_mode_on == 1:
    bot_logger.setLevel(logging.DEBUG)
    bot_logger.debug("Debug mode on")
else:
    bot_logger.setLevel(logging.INFO)
    bot_logger.info("Debug mode off")



# Setting bot intents (aka permissions)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot class, command sync and startup message
class QnDRPbot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync(guild=GUILD)
        bot_logger.info("Commands synced!")
    async def on_ready(self):
        bot_logger.info(f"Bot online as {bot.user.name}, ready to go!")

# Old command bot prefix, even though we don't use old prefixes,
# this is required for the code to function
# DO NOT touch this unless you want to break stuff
bot = QnDRPbot(command_prefix='!', intents=intents)

# General bot commands

# Troll command
@bot.tree.command(name='give_admin', description='gives u admin 100% no scam', guild=GUILD)
async def give_admin_command(interaction: discord.Interaction):
    bot_logger.info(f"{interaction.user} run the 'give_admin' command! lmao")
    await interaction.response.send_message("https://c.tenor.com/2ZGWjr6AMBAAAAAC/tenor.gif")

# Help command with a list of functions
@bot.tree.command(name='help', description='List of functions and commands', guild=GUILD)
async def help_list(interaction: discord.Interaction):
    bot_logger.info(f"{interaction.user} run the 'help' command!")
    help_view = HelpComponent()
    await interaction.response.send_message(view=help_view, ephemeral=True)

# Dice roll related commands

# Listing out available dice
@bot.tree.command(name='dice_list', description='List available dice', guild=GUILD)
async def dice_list_out(interaction: discord.Interaction):
    bot_logger.info(f"{interaction.user} run the 'dice_list' command!")
    get_dice_list_result = get_dice_list()
    await interaction.response.send_message(f"List of available dice:\n {get_dice_list_result }", ephemeral=True)

# (not so) Simple dice roll command with proficiency bonuses
@bot.tree.command(name='roll', description='A simple dice roll with optional proficiency modifiers (+, -)', guild=GUILD)
async def simple_roll_command(interaction: discord.Interaction, dice:str, prof:str | None = None):
    bot_logger.info(f"{interaction.user} run the 'roll' command!")
    bot_logger.debug(f"{interaction.user} input - Dice: {dice} Prof: {prof}")

    # Die validation
    die = get_dice(dice)
    value_check_pass = dice_validation_check(die)
    if value_check_pass is False:
        await interaction.response.send_message("Invalid dice!", ephemeral=True)
        return

    # Dice roll
    die_max = get_max_side(die)
    dice_roll_result = dice_roll(die)

    # Proficiency validation
    if prof is not None:
        bot_logger.debug(f"{interaction.user} used a modifier!")

        #Proficiency value validation
        value_check_pass = proficiency_validation_check(prof)
        if value_check_pass is False:
            await interaction.response.send_message("Invalid proficiency value, this is not a valid number!",ephemeral=True)
            return

        # Proficiency operation validation
        chosen_operation = get_operation(prof[0])
        if chosen_operation is None:
            await interaction.response.send_message("Invalid operation type!", ephemeral=True)
            return

        # Adding proficiency to the dice roll
        operation_value = int(prof[1:5])
        final_dice_roll_result = proficiency_bonus(chosen_operation, operation_value, dice_roll_result)

        prof = prof[0:5]

        final_dice_roll_result_string = f"{prof}={final_dice_roll_result}"

        bot_logger.debug(f"dice roll result: {dice_roll_result}")
        bot_logger.info(f"final dice roll result: {final_dice_roll_result}")

    else:
        bot_logger.debug(f"{interaction.user} didn't use a modifier!")
        bot_logger.info(f"dice roll result: {dice_roll_result}")
        final_dice_roll_result_string = ""

    # Nat sidebar color
    nat_color = onNat_sidebar_color(die_max, dice_roll_result)
    sidebar_color = nat_color

    # Message component
    roll_view = RollComponent(dice, dice_roll_result, interaction.user, final_dice_roll_result_string, sidebar_color)
    await interaction.response.send_message(view=roll_view)

# Roll multiple dice of the same type and sum up the results
@bot.tree.command(name='mroll', description='Roll multiple dice of the same type', guild=GUILD)
async def roll_multiple_command(interaction: discord.Interaction, dice:str, times:str, prof:str | None = None):
    bot_logger.info(f"{interaction.user} run the 'mroll' command!")
    bot_logger.debug(f"{interaction.user} input - Dice: {dice} Times: {times}")

    # Die validation
    die = get_dice(dice)
    value_check_pass = dice_validation_check(die)
    if value_check_pass is False:
        await interaction.response.send_message("Invalid dice!", ephemeral=True)
        return

    # Times roll value check
    value_check_pass = times_to_roll_validation_check(times)
    if value_check_pass is False:
        await interaction.response.send_message("Invalid operation value specified, must be between 2 and 20!",ephemeral=True)
        return
    elif value_check_pass == "ValueError":
        await interaction.response.send_message("Invalid operation value, this is not a valid number!", ephemeral=True)
        return

    # Performing multiple dice rolls
    times = int(times)
    roll_results = multiple_dice_rolls(times, die)
    roll_results_sum = sum(roll_results)
    bot_logger.info(f"dice roll result: {roll_results_sum}")

    # Proficiency validation
    if prof is not None:
        bot_logger.debug(f"{interaction.user} used a modifier!")

        # Proficiency value validation
        value_check_pass = proficiency_validation_check(prof)
        if value_check_pass is False:
            await interaction.response.send_message("Invalid proficiency value, this is not a valid number!",ephemeral=True)
            return

        # Proficiency operation validation
        chosen_operation = get_operation(prof[0])
        if chosen_operation is None:
            await interaction.response.send_message("Invalid operation type!", ephemeral=True)
            return

        # Adding proficiency to the dice roll
        operation_value = int(prof[1:5])
        dice_roll_result = roll_results_sum
        final_dice_roll_result = proficiency_bonus(chosen_operation, operation_value, dice_roll_result)

        prof = prof[0:5]

        final_dice_roll_result_string = f"{roll_results_sum}{prof}={final_dice_roll_result}"

    else:
        final_dice_roll_result_string = roll_results_sum

    roll_multiple_view = RollMultipleComponent(dice, times, interaction.user, roll_results, final_dice_roll_result_string)
    await interaction.response.send_message(view=roll_multiple_view)

# roll two d6 dice with optional modifiers, entire command is hastily and badly written, I will fix it up later
# oh yea it works but barely, component is FUCKED, but I don't care
@bot.tree.command(name='2d6', description='Roll 2d6 with optional proficiency modifiers (+, -)', guild=GUILD)
async def roll2d6_command(interaction: discord.Interaction, prof: str | None = None):
    bot_logger.info(f"{interaction.user} run the '2d6' command!")

    die = get_dice("d6") #I know this is hacky, but I don't care, I'll make it better later.
    dice = "d6"
    times = 2

    # Performing multiple dice rolls
    times = int(times)
    roll_results = multiple_dice_rolls(times, die)
    roll_results_sum = sum(roll_results)
    bot_logger.info(f"dice roll result: {roll_results_sum}")

    # Proficiency validation
    if prof is not None:
        bot_logger.debug(f"{interaction.user} used a modifier!")

        # Proficiency value validation
        value_check_pass = proficiency_validation_check(prof)
        if value_check_pass is False:
            await interaction.response.send_message("Invalid proficiency value, this is not a valid number!",
                                                    ephemeral=True)
            return

        # Proficiency operation validation
        chosen_operation = get_operation(prof[0])
        if chosen_operation is None:
            await interaction.response.send_message("Invalid operation type!", ephemeral=True)
            return

        # Adding proficiency to the dice roll
        operation_value = int(prof[1:5])
        dice_roll_result = roll_results_sum
        final_dice_roll_result = proficiency_bonus(chosen_operation, operation_value, dice_roll_result)

        prof = prof[0:5]

        final_dice_roll_result_string = f"{roll_results_sum}{prof}={final_dice_roll_result}"

    else:
        final_dice_roll_result_string = roll_results_sum

    roll_multiple_view = RollMultipleComponent(dice, times, interaction.user, roll_results, final_dice_roll_result_string)
    await interaction.response.send_message(view=roll_multiple_view)

    # Coin flip related commands

# Simple coinflip
@bot.tree.command(name='flip', description='simple coin flip', guild=GUILD)
async def coinflip_command(interaction: discord.Interaction):
    bot_logger.info(f"{interaction.user} run the 'flip' command!")
    coinflip_result = coinflip()
    bot_logger.debug(f"Coin flip result: {coinflip_result}")
    await interaction.response.send_message(f"Coin flipped!, it landed on {coinflip_result}")



# Running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)