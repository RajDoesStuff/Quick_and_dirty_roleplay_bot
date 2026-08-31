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

# Operation class
class Operation:
    def __init__(self, symbol):
        self.symbol = symbol
    def __str__(self):
        return self.symbol

# List of operations
operation_list = [
    Operation("+"),
    Operation("-"),
]

# Get the highest value possible of a die roll
def get_max_side(dice):
    die_max_side = dice.sides
    return die_max_side


# Get single die info
def get_dice(dice_name):
    for die in dice_list:
        if die.name == dice_name:
            return die
    return None

# Get operation type
def get_operation(prof):
    for operation in operation_list:
        if operation.symbol == prof:
            return operation
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

# Adding proficiency bonus to a roll
def proficiency_bonus(chosen_operation, operation_value, dice_roll_result):
    if chosen_operation.symbol == "+":
        return dice_roll_result + operation_value
    elif chosen_operation.symbol == "-":
        return dice_roll_result - operation_value
    else:
        return None # This monstrosity is here because in the future I want to add more operations
