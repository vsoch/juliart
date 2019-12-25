# Julia Art "juliart"

[![PyPI version](https://badge.fury.io/py/juliart.svg)](https://pypi.org/project/juliart/)
[![GitHub actions status](https://github.com/vsoch/juliart/workflows/ci/badge.svg?branch=master)](https://github.com/vsoch/juliart/actions?query=branch%3Amaster+workflow%3Aci)

This module is based on the [Color Julia Bot](https://twitter.com/colorjulia_bot)
but intended for command line generation, and with options to customize colors
based on holidays. The name "juliart" is also a play on word (Juliard) to hint
at artsy things.

![img/juliart.png](img/juliart.png)

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
                        [--color {random,pattern,glow,christmas,hanukkah,valentine,halloween,fall,spring}]
                        [--zoom ZOOM]

optional arguments:
  -h, --help            show this help message and exit
  --force, -f           force generation of image if already exists.
  --outfile OUTFILE     the output file to save the image (defaults to
                        randomly generated png)
  --res RES             the resolution to generate (defaults to 1000)
  --color {random,pattern,glow,christmas,hanukkah,valentine,halloween,fall,spring}
                        a theme to color the art (defaults to random colors)
  --zoom ZOOM           the level of zoom (defaults to 1.8)
```


If you use the defaults, it will generate a randomly named image in your
present working directory.

```bash
$ juliart generate
Generating Julia Set...
Saving image to doopy-kerfuffle-5780
```

Otherwise you can do any of the customizations shown above!

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
