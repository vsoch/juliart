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
from random import randint, uniform, choice

from math import sqrt
import os
import shutil
import sys
import tempfile


class JuliaSetAnimation:
    """A JuliaSetAnimation instantiates (and controls) a set of JuliaSet
       instances to generate multiple images, and then assemble them into
       an animation. We take a user requested number of frames, and then
       sample along that range from a randomly chosen value (-1, 1) to 1.
       Since the random values are points along a circle, the user is allowed
       to randomize a single or both dimensions.
    """

    def __init__(
        self,
        resolution=1000,
        color="random",
        iterations=200,
        theme="random",
        rgb=None,
        cleanup=True,
        zoom_max=3,
        zoom_min=0,
    ):

        # Set initial values to randomize across
        self.ca = uniform(-1, 1)
        self.cb = uniform(-1, 1)

        # Ensure zooms are set to reasonable values
        self.zoom_max = max(3, zoom_max)
        self.zoom_min = max(0, zoom_min)
        self.zoom = uniform(self.zoom_min, self.zoom_max)
        self.cleanup = cleanup

        self.resolution = resolution
        self.color = color
        self.theme = theme
        self.iterations = iterations
        self.rgb = rgb

    def __str__(self):
        return "[juliaset-animation][resolution:%s][color:%s][iterations:%s]" % (
            self.resolution,
            self.color,
            self.iterations,
        )

    def __repr__(self):
        return self.__str__()

    def calculate_range(self, value, frames, left_bound=-1, right_bound=1):
        """Given a starting value (value) calculate a range of values
           from that value to either a right or left bound. We choose the bound
           that presents the larger distance to generate greater variation. For
           the circle arguments, this means between -1 and 1.
        """
        distance_left = abs(left_bound - value)
        distance_right = abs(right_bound - value)

        if distance_right > distance_left:
            # Distance from -1 to chosen value (increment will likely be negative)
            increment = (left_bound - value) / frames
        else:
            # Distance from chosen value to end value of 1
            increment = (right_bound - value) / frames

        # Calculate the range
        rangex = [(value + x * increment) for x in range(frames)]

        # reverse if the increment was negative and we randomly decide to
        if increment < 0 and choice([1, 2]) == 1:
            rangex.reverse()

        return rangex

    def generate_animation(
        self,
        iterations=None,
        zoom=1.8,
        outfile=None,
        frames=30,
        randomize_x=True,
        randomize_y=True,
        randomize_zoom=False,
    ):
        """Generate the image. If iterations is not provided, we use the default

           Parameters
           ==========
           iterations: iterations per pixel.
        """
        if not iterations:
            iterations = self.iterations

        try:
            import imageio
        except:
            sys.exit("imageio is required to animate. pip install juliart[animate]")

        # Calculate ranges to iterate across based on frames
        rangey = [self.ca] * frames
        rangex = [self.cb] * frames
        zooms = [zoom] * frames

        # Vary argument only if desired
        if randomize_x:
            rangex = self.calculate_range(self.ca, frames)
        if randomize_y:
            rangey = self.calculate_range(self.cb, frames)
        if randomize_zoom:
            zooms = self.calculate_range(
                self.zoom, frames, left_bound=self.zoom_min, right_bound=self.zoom_max
            )

        # Set the colorbias and glow
        juliaset = JuliaSet(
            resolution=self.resolution,
            color=self.color,
            iterations=self.iterations,
            theme=self.theme,
            rgb=self.rgb,
        )
        colorbias = juliaset.colorbias
        glow = juliaset.glow
        prefix = juliaset.generate_name()

        # Create temporary directory to work in
        tmpdir = tempfile.mkdtemp()

        if not outfile:
            outfile = "%s.gif" % prefix

        # Output file must be a gif
        if not outfile.endswith(".gif"):
            outfile = "%s.gif" % os.path.splitext(outfile)[0]

        print("Generating Julia Set Animation...")

        # Keep list of images, we will add them in reverse to loop the animation
        images = []

        # Go through each frame to generate julia set, write animation as we go
        with imageio.get_writer(outfile, mode="I") as writer:
            for i in range(frames):
                juliaset = JuliaSet(
                    resolution=self.resolution, iterations=self.iterations, quiet=True
                )

                # Set pre-determined color and parameter values
                juliaset.colorbias = colorbias
                juliaset.glow = glow
                juliaset.ca = rangex[i]
                juliaset.cb = rangey[i]
                juliaset.generate_image(zoom=zooms[i])

                # We could easily hand the image data to writer, but this preserves frames if desired
                pngfile = os.path.join(tmpdir, "%s-%s.png" % (prefix, i))
                images.append(pngfile)
                juliaset.save_image(pngfile)
                writer.append_data(imageio.imread(pngfile))

            # Now add the images back (in reverse) to create loop
            while images:
                pngfile = images.pop()
                writer.append_data(imageio.imread(pngfile))

        if self.cleanup:
            print("Cleaning up %s" % tmpdir)
            shutil.rmtree(tmpdir)
        else:
            print("Intermediate .png files are in: %s" % tmpdir)
        print("Animation saved to %s" % outfile)


class JuliaSet:
    """A Julia Set is a function named after a famous mathemetician, I think
       it's considered a kind of fractal art. See details at
       https://en.m.wikipedia.org/wiki/Julia_set. This class is derived
       from https://github.com/Visual-mov/Colorful-Julia
    """

    def __init__(
        self,
        resolution=1000,
        color="random",
        iterations=200,
        theme="random",
        rgb=None,
        quiet=False,
    ):
        self.ca = uniform(-1, 1)
        self.cb = uniform(-1, 1)
        self.quiet = quiet
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

    def print(self, message):
        """A wrapper to print to check if quiet is True, and skip if so.
        """
        if not self.quiet:
            print(message)

    def generate_image(self, iterations=None, zoom=1.8):
        """Generate the image. If iterations is not provided, we use the default

           Parameters
           ==========
           iterations: iterations per pixel.
        """
        if not iterations:
            iterations = self.iterations

        self.print("Generating Julia Set...")
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
            outfile = "%s.png" % self.generate_name()
        print("Saving image to %s" % outfile)
        self.image.save(outfile, "PNG")

    def generate_name(self):
        """Generate a random filename from the Robot Namer
        """
        return RobotNamer().generate()

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
