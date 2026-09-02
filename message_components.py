# Message components that make bot responses look nicer
# Some imports are not used yet, don't touch them please, they will be utilized at some point

import discord
from discord.ext import commands
from discord import ui
from discord.ui import (
    LayoutView,
    Container,
    Section,
    TextDisplay,
    Separator,
    MediaGallery,
    Thumbnail,
    ActionRow,
    Button,
    Select,
)
from discord import SelectOption

from cogs.dice_roller import dice_roll

# Help component layout
class HelpComponent(ui.LayoutView):
    def __init__(self):
        super().__init__()  # timeout in seconds, or None for no timeout

        # Build your layout here and add top-level items
        container = ui.Container(
            ui.TextDisplay("### List of available commands:"),
            ui.TextDisplay("/help"),
            ui.TextDisplay("-# List out available commands"),
            ui.TextDisplay("/dice_list"),
            ui.TextDisplay("-# List out available dice"),
            ui.TextDisplay("/roll"),
            ui.TextDisplay("-# Perform a basic dice roll with a single die, optional proficiency modifier (+, -)"),
            ui.TextDisplay("/rollm"),
            ui.TextDisplay("-# Performs a specified amount of dice rolls on a chosen die")
        )
        container.add_item(ui.TextDisplay("Hello, world! :3c made by raj"))

        self.add_item(container)  # Add container to the LayoutView

# Simple roll component layout
class RollComponent(ui.LayoutView):
    def __init__(self, dice, dice_roll_result, user, final_dice_roll_result_string, sidebar_color):
        super().__init__()

        section = ui.Section(
            ui.TextDisplay(f"### {user.mention}"),
            ui.TextDisplay("### Rolled a dice!"),
            ui.TextDisplay(f"### using {dice} \n ## rolled {dice_roll_result}{final_dice_roll_result_string}!"),
            accessory=ui.Thumbnail(
                media=user.display_avatar.url,
            )
        )
        if sidebar_color is not None:
            container = ui.Container(
                section,
                accent_color=discord.Colour.from_rgb(*sidebar_color)
            )
        else:
            container = ui.Container(
                section
            )

        self.add_item(container)

class RollMultipleComponent(ui.LayoutView):
    def __init__(self, dice, times, user, roll_results, roll_results_sum,):
        super().__init__()

        section = ui.Section(
            ui.TextDisplay(f"### {user.mention}"),
            ui.TextDisplay(f"### Rolled a dice {times} times!"),
            ui.TextDisplay(f"### using {dice} \n ## rolled {roll_results}! \n that sums up to {roll_results_sum}!"),
            accessory=ui.Thumbnail(
                media=user.display_avatar.url,
            )
        )

        container = ui.Container(
            section
        )

        self.add_item(container)

class Roll2D6Component(ui.LayoutView):
    def __init__(self, dice, roll_results, user, final_dice_roll_result_string):
        super().__init__()

        section = ui.Section(
            ui.TextDisplay(f"### {user.mention}"),
            ui.TextDisplay("### Rolled a dice!"),
            ui.TextDisplay(f"### using {dice} \n ## rolled {final_dice_roll_result_string} {roll_results} !"),
            accessory=ui.Thumbnail(
                media=user.display_avatar.url,
            )
        )
        container = ui.Container(
            section
        )


        self.add_item(container)