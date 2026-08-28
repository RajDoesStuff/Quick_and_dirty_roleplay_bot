# Dice roller
import random

# Die class
class Dice:
    def __init__(self, name, sides):
        self.sides = sides
        self.name = name
    def __str__(self):
        return self.name

# Die list dice(name, number of sides)
dice_list = [
    Dice("d4", 4),
    Dice("d6", 6),
    Dice("d8", 8),
    Dice("d10", 10),
    Dice("d12", 12),
    Dice("d20", 20),
    Dice("d100", 100),
]

# Get single die info
def get_dice(dice_name):
    for die in dice_list:
        if die.name == dice.name:
            return die
    return None

# Get entire die list
def get_dice_list():
    print("Dice list:")
    for dice in dice_list:
        print(dice)
    return ", ".join(str(dice) for dice in dice_list)

# Simple die roll
def dice_roll(dice):
    roll = random.randint(1, dice.sides)
    return roll

# Advanced die roll - not done yet
def advanced_dice_roll(expression):
    result = read_dice_term(expression)
    return result

# Reading expressions - this is complete bullshit, no done yet, no clue what I'm doing here lmao
def read_dice_term(term):
    if "d" not in term:
        return None
    multiplier, dice_name = term.split("d", 1)
    if multiplier == "":
        multiplier = 1
    else:
        multiplier = int(multiplier)
    dice_name = "d" + dice_name
    dice = get_dice(dice_name)
    if dice is None:
        return None

    return multiplier, dice