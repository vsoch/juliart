"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from .namer import RobotNamer
from .colors import get_theme_colors
from PIL import Image, ImageDraw
from random import randint, uniform

from math import sqrt
import os
import sys


class JuliaSet:
    """A Julia Set is a function named after a famous mathemetician, I think
       it's considered a kind of fractal art. See details at
       https://en.m.wikipedia.org/wiki/Julia_set. This class is derived
       from https://github.com/Visual-mov/Colorful-Julia
    """

    def __init__(
        self, resolution=1000, color="random", iterations=200, theme="random", rgb=None
    ):
        self.ca = uniform(-1, 1)
        self.cb = uniform(-1, 1)
        self.res = (resolution, resolution)
        self.color = color
        self.theme = theme
        self.iterations = iterations
        self.image = Image.new("RGB", self.res)
        self.draw = ImageDraw.Draw(self.image)
        self.generate_colors(rgb)

    def __str__(self):
        return "[juliaset][resolution:%s][color:%s][iterations:%s]" % (
            self.res,
            self.color,
            self.iterations,
        )

    def __repr__(self):
        return self.__str__()

    def generate_colors(self, rgb):
        """Re-generate colorbias and glow.
        """
        # Themes are relevant for any color choice other than glow
        if self.theme == "random":
            if rgb is not None:
                try:
                    self.colorbias = tuple([int(x.strip()) for x in rgb.split(",")])
                except:
                    sys.exit("Error parsing %s, ensure is comma separated numbers.")
            else:
                self.colorbias = (
                    self.rnd(20, 200),
                    self.rnd(20, 200),
                    self.rnd(20, 200),
                )
        else:
            self.colorbias = get_theme_colors(self.theme)
        self.glow = (self.rnd(0, 10), self.rnd(0, 10), self.rnd(0, 10))

    def generate_image(self, iterations=None, zoom=1.8):
        """Generate the image. If iterations is not provided, we use the default

           Parameters
           ==========
           iterations: iterations per pixel.
        """
        if not iterations:
            iterations = self.iterations

        print("Generating Julia Set...")
        for x in range(self.res[0]):
            for y in range(self.res[1]):
                za = self.translate(x, 0, self.res[0], -zoom, zoom)
                zb = self.translate(y, 0, self.res[1], -zoom, zoom)
                i = 0
                while i < iterations:
                    tmp = 2 * za * zb
                    za = za * za - zb * zb + self.ca
                    zb = tmp + self.cb
                    if sqrt(za * za + zb * zb) > 4:
                        break
                    i += 1
                self.draw.point(
                    (x, y),
                    self.colorize(i, iterations) if i != iterations else (0, 0, 0),
                )

    def save_image(self, outfile=None):
        """Save the image to an output file, if provided.
        """
        if not outfile:
            outfile = self.generate_name()
        print("Saving image to %s" % outfile)
        self.image.save(outfile, "PNG")

    def generate_name(self):
        """Generate a random filename from the Robot Namer
        """
        return "%s.png" % RobotNamer().generate()

    def colorize(self, i, iterations=None):
        """Based on the user selection, save with a pattern, random, or glowing color
        """
        if not iterations:
            iterations = self.iterations

        if self.color == "random":
            c = int(self.translate(i, 0, iterations, 0, 255) * (i / 4))
            return (c + self.colorbias[0], c + self.colorbias[1], c + self.colorbias[2])

        elif self.color == "pattern":
            if i % 2 == 0:
                return self.colorbias
            return (0, 0, 0)

        elif self.color == "glow":
            return (i * self.glow[0], i * self.glow[1], i * self.glow[2])

        else:
            print("Color choice %s is not valid." % self.color)
            sys.exit(1)

    def rnd(self, a, b):
        return randint(a, b)

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        return rightMin + (
            float(value - leftMin) / float(leftMax - leftMin) * (rightMax - rightMin)
        )
