"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from random import randint, choice
import os
import sys

christmas_colors = [
    (179, 0, 12),
    (220, 61, 42),
    (13, 239, 66),
    (0, 179, 44),
    (13, 89, 1),
]
hanukkah_colors = [
    (9, 35, 155),
    (154, 184, 194),
    (242, 235, 219),
    (242, 205, 60),
    (218, 174, 75),
]
valentine_colors = [
    (94, 8, 30),
    (181, 26, 58),
    (226, 71, 103),
    (228, 131, 151),
    (228, 205, 211),
]
halloween_colors = [
    (247, 95, 28),
    (255, 154, 0),
    (0, 0, 0),
    (136, 30, 228),
    (133, 226, 31),
]
fall_colors = [(96, 60, 20), (156, 39, 6), (212, 91, 18), (243, 188, 46), (95, 84, 38)]
summer_colors = [
    (35, 110, 150),
    (21, 178, 211),
    (255, 215, 0),
    (243, 135, 47),
    (255, 89, 143),
]
spring_colors = [
    (243, 168, 188),
    (245, 173, 148),
    (255, 241, 166),
    (180, 249, 165),
    (158, 231, 245),
]
winter_colors = [
    (66, 104, 124),
    (132, 165, 184),
    (179, 218, 241),
    (203, 203, 203),
    (112, 117, 113),
]
easter_colors = [
    (255, 212, 229),
    (224, 205, 255),
    (189, 232, 239),
    (183, 215, 132),
    (254, 255, 162),
]
thanksgiving_colors = [
    (108, 47, 0),
    (158, 104, 42),
    (241, 185, 48),
    (181, 71, 48),
    (138, 151, 72),
]


def get_theme_colors(theme):
    """Return a color from a themed set, the default being a random color
    """
    if theme == "christmas":
        return choice(christmas_colors)
    elif theme == "easter":
        return choice(easter_colors)
    elif theme == "fall":
        return choice(fall_colors)
    elif theme == "halloween":
        return choice(halloween_colors)
    elif theme == "hanukkah":
        return choice(hanukkah_colors)
    elif theme == "spring":
        return choice(spring_colors)
    elif theme == "summer":
        return choice(summer_colors)
    elif theme == "thanksgiving":
        return choice(thanksgiving_colors)
    elif theme == "valentine":
        return choice(valentine_colors)
    elif theme == "winter":
        return choice(winter_colors)
    else:
        return (randint(20, 200), randint(20, 200), randint(20, 200))
