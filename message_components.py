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
            ui.TextDisplay("-# Perform a basic dice roll with a single die"),
        )
        container.add_item(ui.TextDisplay("Hello, world! :3c"))

        self.add_item(container)  # Add container to the LayoutView

# Simple roll component layout
class RollComponent(ui.LayoutView):
    def __init__(self, dice, dice_roll_result, user):
        super().__init__()

        section = ui.Section(
            ui.TextDisplay(f"### {user.mention}"),
            ui.TextDisplay("### Rolled a dice!"),
            ui.TextDisplay(f"### using {dice} \n ## rolled {dice_roll_result}!"),
            accessory=ui.Thumbnail(
                media=user.display_avatar.url,
            )
        )
        container = ui.Container(
            section
        )
        self.add_item(container)