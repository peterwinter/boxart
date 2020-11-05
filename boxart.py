import random
import numpy as np
import pandas as pd

n_low = 3
n_high = 5
n_start = 4

def next_cut_n(current_n):
    """
    """
    r = random.random()
    if r <= 0.5:
        return current_n
    else:
        if current_n == n_high:
            return current_n - 1
        elif current_n == n_low:
            return current_n + 1
        else:
            if r < 0.75:
                return current_n - 1
            else:
                return current_n + 1

def make_cuts(n=4, last_cuts=[]):
    """
    """
    p_last = 0.4
    p_prev = 0.4
    # random between 0-100
    # Look at last step. -> each gets kept 40%
    # look at step before last -> each gets kept 40%

    new_cuts = np.random.randint(0, 100, n)
    while len(new_cuts) > len(set(new_cuts)):
        new_cuts = np.random.randint(0, 100, n)

    new_cuts.sort()
    return new_cuts.tolist()

def cuts_to_blocks(x, cuts):
    c = [0] + cuts + [100]
    blocks = []
    for i, (y0, y1) in enumerate(zip(c[:], c[1:])):
        b = {'id': f"{x}{i}",
             'x': x,
             'y0': y0,
             'y1': y1,
            }
        blocks.append(b)
    return blocks


def make_step(last_step=None):

    if last_step is None:
        last_step = {
            'x': -1,
            'n': n_start,
            'cuts': make_cuts(n_start),
        }

    current_n = next_cut_n(last_step['n'])
    cuts = make_cuts(n=current_n, last_cuts=last_step['cuts'])
    x = last_step['x'] + 1
    blocks = cuts_to_blocks(x, cuts)

    s = {
        "x": x,
        "n":current_n,
        "cuts": cuts,
        "blocks": blocks,
#         "patches": blocks_to_patches(blocks),
        }
    return s

def make_blocks(n_cols):
    steps = []
    blocks = []

    last_step = None
    for i in range(n_cols):
        s = make_step(last_step=last_step)
        blocks += s['blocks']
        steps.append(s)
        last_step = s

    return blocks