# Coin flipper

import random

def coinflip():
    flip_result = random.randint(0, 1)
    print (flip_result)
    if flip_result == 1:
        flip_result = "heads"
        return flip_result
    else:
        flip_result = "tails"
        return flip_result
