# Julia Art "juliart"

[![PyPI version](https://badge.fury.io/py/juliart.svg)](https://pypi.org/project/juliart/)
[![GitHub actions status](https://github.com/vsoch/juliart/workflows/ci/badge.svg?branch=master)](https://github.com/vsoch/juliart/actions?query=branch%3Amaster+workflow%3Aci)

This module is based on the [Color Julia Bot](https://twitter.com/colorjulia_bot)
but intended for command line generation, and with options to customize colors
based on holidays. The name "juliart" is also a play on word (Juliard) to hint
at artsy things.

![img/juliart.png](https://raw.githubusercontent.com/vsoch/juliart/master/img/juliart.png)

I'm customizing it to add more color palette choices (under development).

## Usage

### Install

You can install from pypi

```bash
pip install juliart
```

or install from the repository directly:

```bash
$ git clone https://github.com/vsoch/juliart
$ python setup.py install
```

### Generate Art

You can see basic usage by typing `juliart` into your terminal:

```bash
$ juliart
usage: juliart [-h] [--version] {generate} ...

Julia Set art generator

optional arguments:
  -h, --help  show this help message and exit
  --version   suppress additional output.

actions:
  actions for Julia Set art generator

  {generate}  juliart actions
    generate  generate a Julia Set image
```

And then customizations for the generate command:

```bash
$ juliart generate --help
usage: juliart generate [-h] [--force] [--outfile OUTFILE] [--res RES]
                        [--color {random,pattern,glow}]
                        [--theme {christmas,easter,fall,random,halloween,hanukkah,spring,summer,thanksgiving,valentine,winter}]
                        [--zoom ZOOM]

optional arguments:
  -h, --help            show this help message and exit
  --force, -f           force generation of image if already exists.
  --outfile OUTFILE     the output file to save the image (defaults to
                        randomly generated png)
  --res RES             the resolution to generate (defaults to 1000)
  --color {random,pattern,glow}
                        a color pattern to follow.
  --theme {christmas,easter,fall,random,halloween,hanukkah,spring,summer,thanksgiving,valentine,winter}
                        a theme to color the art (defaults to random colors)
  --zoom ZOOM           the level of zoom (defaults to 1.8)
```

If you use the defaults, it will generate a randomly named image in your
present working directory.

```bash
$ juliart generate
Generating Julia Set...
Saving image to doopy-kerfuffle-5780.png
```

Otherwise you can do any of the customizations shown above!

### Colors

The three choices for colors are random, pattern, or glow, or setting your
own RGB value.

#### Random

Random is the default, and the image at the top of the README here is generated using
this setting. Take a look at more [more random examples](https://github.com/vsoch/juliart/tree/master/img/random).

#### Pattern

Pattern doesn't use a gradual gradient, but instead returns a hard boundary between
a color (and black). 

![img/pattern/delicious-lizard-8995.png](https://raw.githubusercontent.com/vsoch/juliart/master/img/pattern/delicious-lizard-8995.png)

Take a look at more [more pattern examples](https://github.com/vsoch/juliart/tree/master/img/pattern) here.

### RGB

If you want complete control of the color, provide a comma separated list
of RGB numbers as follows:

```bash
$ juliart generate --rgb 9,35,155
```

Note that this will also work with the `--color pattern` flag.

#### Glow

Glow means a dark background (black) with a color gradient. Here is an example:

![img/glow/dinosaur-diablo-1189.png](https://raw.githubusercontent.com/vsoch/juliart/master/img/glow/dinosaur-diablo-1189.png)

And is generated as follows:

```bash
juliart generate --color glow
```

See [more glow examples](https://github.com/vsoch/juliart/tree/master/img/glow).

If you choose glow, this will overwrite the choice of a theme (discussed next).

### Themes

To get a little more variety in your choice of colors, you can select a theme! 

```bash
juliart generate --theme halloween
juliart generate --theme christmas
juliart generate --theme hanukkah
juliart generate --theme thanksgiving
juliart generate --theme valentine

juliart generate --theme easter
juliart generate --theme fall
juliart generate --theme spring
juliart generate --theme summer
juliart generate --theme winter
```

For any of the commands above, you can also add `--color pattern` to flip the background
from the theme color to be black. 

```bash
$ juliart generate --theme halloween --color pattern
```

Take a look at images in the [themes folder](https://github.com/vsoch/juliart/tree/master/img/pattern) 
to get a sense of the color palettes.

### Docker

You can run the pre-generated Docker container too! You'll need to bind a folder
on the host to save the image to.

```bash
$ mkdir data
$ docker run -it -v $PWD/data/:/data vanessa/juliart generate --outfile /data/art.png
```

You can also build the image first if you like:

```bash
$ docker build -t vanessa/juliart .
```
