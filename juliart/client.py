#!/usr/bin/env python

"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from juliart.main import JuliaSet, JuliaSetAnimation
import juliart
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="Julia Set art generator")
    parser.add_argument(
        "--version",
        dest="version",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    description = "actions for Julia Set art generator"
    subparsers = parser.add_subparsers(
        help="juliart actions", title="actions", description=description, dest="command"
    )

    generate = subparsers.add_parser("generate", help="generate a Julia Set image")
    animate = subparsers.add_parser(
        "animate", help="create a Julia Set animation (gif)"
    )

    generate.add_argument(
        "--radius",
        dest="radius",
        help="the max radius to allow (default is 4)",
        type=int,
        default=4,
    )

    animate.add_argument(
        "--no-cleanup",
        dest="skip_cleanup",
        help="Do not delete temporary directory with png files to generate gif.",
        default=False,
        action="store_true",
    )

    animate.add_argument(
        "--constant-a",
        dest="constant_a",
        help="Don't randomize the point A on the circle.",
        default=False,
        action="store_true",
    )

    animate.add_argument(
        "--constant-b",
        dest="constant_b",
        help="Don't randomize the point B on the circle.",
        default=False,
        action="store_true",
    )

    animate.add_argument(
        "--randomize-zoom",
        dest="randomize_zoom",
        help="Randomize the zoom up to --zoom-min or --zoom-max.",
        default=False,
        action="store_true",
    )

    animate.add_argument(
        "--zoom-max",
        dest="zoom_max",
        help="the max zoom (must be greater than 3)",
        type=int,
        default=3,
    )

    animate.add_argument(
        "--zoom-min",
        dest="zoom_min",
        help="the max zoom (must be greater than 0)",
        type=int,
        default=0,
    )

    animate.add_argument(
        "--frames",
        dest="frames",
        help="the number of frames to generate (default is 30)",
        type=int,
        default=30,
    )

    for subparser in [generate, animate]:
        subparser.add_argument(
            "--outfile",
            dest="outfile",
            help="the output file to save the image (defaults to randomly generated png)",
            type=str,
            default=None,
        )

        ## Text

        subparser.add_argument(
            "--text",
            dest="text",
            help="write a string of text to bottom left corner",
            type=str,
            default=None,
        )

        subparser.add_argument(
            "--fontsize",
            dest="fontsize",
            help="font size of text (if desired) defaults to 16",
            type=int,
            default=16,
        )

        subparser.add_argument(
            "--font",
            dest="font",
            help="choice of font (defaults to open sans)",
            type=str,
            choices=["OpenSans-Regular", "Pacifico-Regular"],
            default="OpenSans-Regular",
        )

        subparser.add_argument(
            "--font-alpha",
            dest="font_alpha",
            help="font transparency (defaults to 1)",
            type=int,
            default=100,
        )

        subparser.add_argument(
            "--xcoord",
            dest="xcoord",
            help="x coordinate for text (defaults to 0)",
            type=int,
            default=10,
        )

        subparser.add_argument(
            "--ycoord",
            dest="ycoord",
            help="y coordinate for text (defaults to 0)",
            type=int,
            default=10,
        )

        subparser.add_argument(
            "--ca",
            dest="ca",
            help="the a component of the c parameter",
            type=float,
            default=None,
        )

        subparser.add_argument(
            "--cb",
            dest="cb",
            help="the b component of the c parameter",
            type=float,
            default=None,
        )

        subparser.add_argument(
            "--res",
            dest="res",
            help="the resolution to generate (defaults to 1000)",
            type=int,
            default=1000,
        )

        subparser.add_argument(
            "--iter",
            dest="iters",
            help="the number of iterations per pixel (defaults to 200)",
            type=int,
            default=200,
        )

        subparser.add_argument(
            "--color",
            dest="color",
            choices=["random", "pattern", "glow"],
            help="a color pattern to follow.",
            type=str,
            default="random",
        )

        subparser.add_argument(
            "--rgb",
            dest="rgb",
            help="a specific rbg color, in format R,G,B",
            type=str,
            default=None,
        )

        subparser.add_argument(
            "--theme",
            dest="theme",
            choices=[
                "christmas",
                "easter",
                "fall",
                "random",
                "halloween",
                "hanukkah",
                "spring",
                "summer",
                "thanksgiving",
                "valentine",
                "winter",
            ],
            help="a theme to color the art (defaults to random colors)",
            type=str,
            default="random",
        )

        subparser.add_argument(
            "--zoom",
            dest="zoom",
            help="the level of zoom (defaults to 1.8)",
            type=float,
            default=1.8,
        )

    return parser


def main():
    """main is the entrypoint to the juliart client.
    """

    parser = get_parser()

    # Will exit with subcommand help if doesn't parse
    args, extra = parser.parse_known_args()

    # Show the version and exit
    if args.version:
        print(juliart.__version__)
        sys.exit(0)

    # If the provided font doesn't end in ttf
    if hasattr(args, 'font'):
        font = args.font
        if not args.font.endswith(".ttf"):
            font = "%s.ttf" % (font)

    # Initialize the JuliaSet
    if args.command == "generate":
        juliaset = JuliaSet(
            resolution=args.res,
            color=args.color,
            ca=args.ca,
            cb=args.cb,
            theme=args.theme,
            rgb=args.rgb,
            iterations=args.iters,
        )
        juliaset.generate_image(zoom=args.zoom, radius=args.radius)

        # Add text, if the user wants to (args.text will be checked to be None)
        juliaset.write_text(
            args.text,
            fontsize=args.fontsize,
            xcoord=args.xcoord,
            ycoord=args.ycoord,
            font=font,
            rgb=(255, 255, 255, args.font_alpha),
        )

        juliaset.save_image(args.outfile)

    elif args.command == "animate":

        # Takes similar args to JuliaSet, but also animation preferences
        juliaset = JuliaSetAnimation(
            resolution=args.res,
            color=args.color,
            theme=args.theme,
            rgb=args.rgb,
            ca=args.ca,
            cb=args.cb,
            cleanup=not args.skip_cleanup,
            iterations=args.iters,
            zoom_max=args.zoom_max,
            zoom_min=args.zoom_min,
        )

        juliaset.generate_animation(
            zoom=args.zoom,
            outfile=args.outfile,
            frames=args.frames,
            randomize_a=not args.constant_a,
            randomize_b=not args.constant_b,
            randomize_zoom=args.randomize_zoom,
            text=args.text,
            font=font,
            fontalpha=args.font_alpha,
            fontsize=args.fontsize,
            xcoord=args.xcoord,
            ycoord=args.ycoord,
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
