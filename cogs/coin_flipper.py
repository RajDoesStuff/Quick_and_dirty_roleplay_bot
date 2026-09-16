# Coin flipper

import random
import logging

logger = logging.getLogger(f"Bot.{__name__}")

def coinflip():
    logging.debug("performing a coinflip")
    poop_value = random.randint(0, 299) #I am the poopster, very mature poopster
    if poop_value == 299:
        return "its side, fuck you"
    else:
        flip_result = random.randint(0, 1)
        print (flip_result)
        if flip_result == 1:
            flip_result = "heads"
            return flip_result
        else:
            flip_result = "tails"
            return flip_result
