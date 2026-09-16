# Dice roller
import random
import logging



# Logging
logger = logging.getLogger(f"Bot.{__name__}")


# Die class
class Dice:
    def __init__(self, name, sides):
        self.sides = sides
        self.name = name
    def __str__(self):
        return self.name

# Die list dice(name, number of sides)
dice_list = [
    Dice("d3", 3),
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

# Info fetchers
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
    logger.debug("running get operation check")
    for operation in operation_list:
        if operation.symbol == prof:
            logger.debug("Valid operation found, moving on")
            return operation
    logger.debug("invalid operation type specified!")
    return None

# Get entire die list
def get_dice_list():
    print("Dice list:")
    for dice in dice_list:
        print(dice)
    return ", ".join(str(dice) for dice in dice_list)

#Data Validators
#Dice list validation check
def dice_validation_check(die):
    logger.debug("running dice validation check")
    if die is None:
        logger.debug(f"used an invalid dice!")
        is_die_valid = False
        return is_die_valid
    else:
        logger.debug("Validation check passed!")
        is_die_valid = True
        return is_die_valid

# Proficiency validation check
def proficiency_validation_check(prof):
    logger.debug("running proficiency validation check")
    try:
        operation_value = int(prof[1:5])
        if operation_value is None:
            logger.debug(f"Didn't specify a value! {operation_value}")
            is_valid = False
            return is_valid
    except ValueError:
        logger.debug(f"used an invalid value! {prof}")
        is_valid = False
        return is_valid
    else:
        logger.debug("Validation check passed!")
        is_valid = True
        return is_valid

# Roll multiple times to roll value validation check
def times_to_roll_validation_check(times):
    logger.debug("running times to roll validation check")
    try:
        times = int(times)
        if times <= 1 or times >= 21:
            logger.debug("used an invalid value range!")
            is_times_valid = False
            return is_times_valid
        else:
            logger.debug("Validation check passed!")
            is_times_valid = True
            return is_times_valid
    except ValueError:
        logger.debug(f" Value error, used an invalid value!")
        is_times_valid = "ValueError"
        return is_times_valid


# Math related
# Simple die roll
def dice_roll(dice):
    roll = random.randint(1, dice.sides)
    return roll

def multiple_dice_rolls(times, die):
    roll_results = []
    for _ in range(0, times):
        roll_result = dice_roll(die)
        roll_results.append(roll_result)
    return roll_results

# Adding proficiency bonus to a roll result
def proficiency_bonus(chosen_operation, operation_value, dice_roll_result):
    if chosen_operation.symbol == "+":
        return dice_roll_result + operation_value
    elif chosen_operation.symbol == "-":
        return dice_roll_result - operation_value
    else:
        return None # This monstrosity is here because in the future I want to add more operations

# Setting the sidebar color
def onNat_sidebar_color(die_max, dice_roll_result):
    if dice_roll_result == 1:
        nat_color = [209, 19, 19]
        return nat_color
    elif dice_roll_result == die_max:
        nat_color = [30, 212, 78]
        return nat_color
    else:
        return None