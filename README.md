# Julia Art "juliart"

[![PyPI version](https://badge.fury.io/py/juliart.svg)](https://pypi.org/project/juliart/)
[![GitHub actions status](https://github.com/vsoch/juliart/workflows/ci/badge.svg?branch=master)](https://github.com/vsoch/juliart/actions?query=branch%3Amaster+workflow%3Aci)

This module is based on the [Color Julia Bot](https://twitter.com/colorjulia_bot)
but intended for command line generation, and with options to customize colors
based on themes (holidays, seasons) and also generate animations. 
The name "juliart" is also a play on word (Juliard) to hint
at artsy things.

![img/juliart.png](https://raw.githubusercontent.com/vsoch/juliart/master/img/juliart.png)

I've done my best so that the default parameters produce (what I think to be)
the most random and pretty images. You can of course tweak the parameters
to your liking, discussed below!

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

for animations you'll also need an extra package:

```bash
pip install juliart[animate]
```

### Generate Art

You can see basic usage by typing `juliart` into your terminal:

```bash
$ juliart
usage: juliart [-h] [--version] {generate,animate} ...

Julia Set art generator

optional arguments:
  -h, --help          show this help message and exit
  --version           suppress additional output.

actions:
  actions for Julia Set art generator

  {generate,animate}  juliart actions
    generate          generate a Julia Set image
    animate           create a Julia Set animation (gif)
```

You'll see there are two options: to generate, and to animate. 


#### Generate

Customizations for the generate command generally include color or theme choices,
an optional text to print on the graphic, and parameters.


```bash
$ juliart generate --help
usage: juliart generate [-h] [--radius RADIUS] [--outfile OUTFILE]
                        [--text TEXT] [--fontsize FONTSIZE] [--xcoord XCOORD]
                        [--ycoord YCOORD] [--ca CA] [--cb CB] [--res RES]
                        [--iter ITERS] [--color {random,pattern,glow}]
                        [--rgb RGB]
                        [--theme {christmas,easter,fall,random,halloween,hanukkah,spring,summer,thanksgiving,valentine,winter}]
                        [--zoom ZOOM]

optional arguments:
  -h, --help            show this help message and exit
  --radius RADIUS       the max radius to allow (default is 4)
  --outfile OUTFILE     the output file to save the image (defaults to
                        randomly generated png)
  --text TEXT           write a string of text to bottom left corner
  --fontsize FONTSIZE   font size of text (if desired) defaults to 16
  --xcoord XCOORD       x coordinate for text (defaults to 0)
  --ycoord YCOORD       y coordinate for text (defaults to 0)
  --ca CA               the a component of the c parameter
  --cb CB               the b component of the c parameter
  --res RES             the resolution to generate (defaults to 1000)
  --iter ITERS          the number of iterations per pixel (defaults to 200)
  --color {random,pattern,glow}
                        a color pattern to follow.
  --rgb RGB             a specific rbg color, in format R,G,B
  --theme {christmas,easter,fall,random,halloween,hanukkah,spring,summer,thanksgiving,valentine,winter}
                        a theme to color the art (defaults to random colors)
  --zoom ZOOM           the level of zoom (defaults to 1.8)
```

##### Defaults

If you use the defaults, it will generate a randomly named image in your
present working directory.

```bash
$ juliart generate
Generating Julia Set...
Saving image to doopy-kerfuffle-5780.png
```

##### C Parameters

The values of ca and cb (the real and complex components of the c parameter
in the Julia Set equation) are chosen at random, but you can select them
to better understand how your choices influence the graphic generation:

```bash
juliart generate --ca 0.5 --cb 0.5
```

I also created a [small project](https://github.com/vsoch/juliart-grid/) that will visually show how your parameter selection
influences the resulting image! You might want to give the output file a more meaningful name:

```bash
juliart generate --ca 0.5 --cb 0.5 --outfile ca-0.5-cb-0.5.png
```

And if you intend to compare the images, setting a consistent color is also 
reasonable:

```bash
juliart generate --ca 0.5 --cb 0.5 --outfile ca-0.5-cb-0.5.png --rgb 90,12,10
```

For a bigger deep dive into this exercise (I was curious) see [Juliart Grid](https://github.com/vsoch/juliart-grid).


##### Text

As an alternative to file name (or just to have some fun!) you can generate
an image with a custom message.

```bash
juliart generate --text "Dinosaurs are great!"
```

By default the text will be printed in the top left corner (coordinate 10,10)
however you can adjust this to your liking:

```bash
$ juliart generate --text "Avocados are also great!" --xcoord 200 --ycoord 20
```

You can see both of these examples in the [text](img/text) examples folder.


##### Zoom, Iterations, and Radius

Otherwise you can do any of the customizations shown above! Try playing
around with iterations, colors/themes, and zoom to see different effects.

```bash
$ juliart generate --zoom 3
$ juliart generate --iter 100
```

After looking over the equation to generate the JuliaSet for a while,
I got the insight that if we increase the iterations value and modify the radious,
 this will generate more detailed images. Here are some examples:

```bash
juliart generate --iter 1000 --radius 8
```

![img/random/frigid-kitty-0005.png](https://raw.githubusercontent.com/vsoch/juliart/master/img/random/frigid-kitty-0005.png)

```bash
juliart generate --iter 5000 --radius 10
```

This one takes longer, of course.

To generate from within Python, here is a quick example:

```python
from juliart.main import JuliaSet

juliaset = JuliaSet(
    resolution=1000, # (1000x1000)
    color="random", # random, glow, pattern
    theme="random",
    rgb=None,  # "197,18,12"
    iterations=200,
)
juliaset.generate_image(zoom=1.8)
juliaset.save_image("/tmp/myimage.png")
```

#### Animate

![img/animate/butterscotch-plant-7505.gif](https://raw.githubusercontent.com/vsoch/juliart/master/img/animate/butterscotch-plant-7505.gif)

You can inspect the parameters for the animation command as follows:

```bash
$ juliart animate --help
usage: juliart animate [-h] [--no-cleanup] [--constant-a] [--constant-b]
                       [--randomize-zoom] [--zoom-max ZOOM_MAX]
                       [--zoom-min ZOOM_MIN] [--frames FRAMES]
                       [--outfile OUTFILE] [--text TEXT] [--fontsize FONTSIZE]
                       [--xcoord XCOORD] [--ycoord YCOORD] [--ca CA] [--cb CB]
                       [--res RES] [--iter ITERS]
                       [--color {random,pattern,glow}] [--rgb RGB]
                       [--theme {christmas,easter,fall,random,halloween,hanukkah,spring,summer,thanksgiving,valentine,winter}]
                       [--zoom ZOOM]

optional arguments:
  -h, --help            show this help message and exit
  --no-cleanup          Do not delete temporary directory with png files to
                        generate gif.
  --constant-a          Don't randomize the point A on the circle.
  --constant-b          Don't randomize the point B on the circle.
  --randomize-zoom      Randomize the zoom up to --zoom-min or --zoom-max.
  --zoom-max ZOOM_MAX   the max zoom (must be greater than 3)
  --zoom-min ZOOM_MIN   the max zoom (must be greater than 0)
  --frames FRAMES       the number of frames to generate (default is 30)
  --outfile OUTFILE     the output file to save the image (defaults to
                        randomly generated png)
  --text TEXT           write a string of text to bottom left corner
  --fontsize FONTSIZE   font size of text (if desired) defaults to 16
  --xcoord XCOORD       x coordinate for text (defaults to 0)
  --ycoord YCOORD       y coordinate for text (defaults to 0)
  --ca CA               the a component of the c parameter
  --cb CB               the b component of the c parameter
  --res RES             the resolution to generate (defaults to 1000)
  --iter ITERS          the number of iterations per pixel (defaults to 200)
  --color {random,pattern,glow}
                        a color pattern to follow.
  --rgb RGB             a specific rbg color, in format R,G,B
  --theme {christmas,easter,fall,random,halloween,hanukkah,spring,summer,thanksgiving,valentine,winter}
                        a theme to color the art (defaults to random colors)
  --zoom ZOOM           the level of zoom (defaults to 1.8)
```

Most of these defaults (mins and maxes) are fairly reasonable and you wouldn't
want to change them. By default, we will vary both the A and B constants that
are used to generate the Julia Set, but we won't vary the zoom. 

##### Defaults

The defaults will generate a 30 framed animation, varying the parameters
A and B but not the zoom, with resolution (1000 X 1000) and 200 iterations.

```bash
$ juliart animate --frames 5
```

##### Optimize 

You can make that faster by changing the iterations and resolution, of course!

```bash
$ juliart animate --res 500 --iters 100
```

The tradeoff is image quality. You'll also notice in the case of generating
black pixels it takes slightly longer than white pixels (since white is 
an absence of color).

##### Text

You can add a consistent message to all frames in an animation:

```bash
juliart animate --text "Dinosaurs are great!"
```

and customize the `--xcoord`, `--ycoord`, or `--fontsize` parameters as
desired. See the [text](img/text) examples folder for an example. If you want
to vary the text between frames, then you'll need to roll your own
loop to generate the frames and then combine into an animation. An example
is provided, the code at [Juliart Grid](https://github.com/vsoch/juliart-grid).


##### Cleanup

If you want to keep the temporary png images (the frames) you can do:

```bash
$ juliart animate --no-cleanup
```

##### Frames

If you want to customize the number of frames, you can do that too (we default to 30). Here
would be a smaller / quicker to generate image:

```bash
$ juliart animate --frames 5
```

##### Zoom

To also randomize the zoom, specify:

```bash
$ juliart animate --randomize-zoom --frames 5
```

##### Python

To generate from within Python, it's fairly straight forward:

```python
from juliart.main import JuliaSetAnimation

juliaset = JuliaSetAnimation(
    resolution=args.res,
    color=args.color,
    theme=args.theme,
    rgb=args.rgb,
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
)
```


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

## Support

Do you have a question? Or want to suggest a feature to make it better?
Please [open an issue!](https://www.github.com/vsoch/juliart)
