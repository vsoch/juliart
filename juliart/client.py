#!/usr/bin/env python

"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from juliart.main import JuliaSet
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
    generate.add_argument(
        "--force",
        "-f",
        dest="force",
        help="force generation of image if already exists.",
        default=False,
        action="store_true",
    )

    generate.add_argument(
        "--outfile",
        dest="outfile",
        help="the output file to save the image (defaults to randomly generated png)",
        type=str,
        default=None,
    )

    generate.add_argument(
        "--res",
        dest="res",
        help="the resolution to generate (defaults to 1000)",
        type=int,
        default=1000,
    )

    generate.add_argument(
        "--color",
        dest="color",
        choices=["random", "pattern", "glow"],
        help="a color pattern to follow.",
        type=str,
        default="random",
    )

    generate.add_argument(
        "--rgb",
        dest="rgb",
        help="a specific rbg color, in format R,G,B",
        type=str,
        default=None,
    )

    generate.add_argument(
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

    generate.add_argument(
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

    # Initialize the JuliaSet
    if args.command == "generate":
        juliaset = JuliaSet(
            resolution=args.res, color=args.color, theme=args.theme, rgb=args.rgb
        )
        juliaset.generate_image(zoom=args.zoom)
        juliaset.save_image(args.outfile)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
