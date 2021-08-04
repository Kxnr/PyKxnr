from pykxnr.utils import clamp

# TODO: make color class


class ColorPalette:
    '''
    Custom type that allows using format strings
    {palette:<color>} and {palette:endcolor}
    to print ansi color codes into output
    '''
    endcolor = '\x1B[m'

    def __init__(self, default=0, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key.lower(), val)
        self.default = default

# FIXME: checking for explicit endcolor is a bit of a hack
class ANSI8ColorPalette(ColorPalette):
    def __format__(value, spec):
        color, *opts = spec.split(':')

        if color == 'endcolor':
            return value.endcolor

        try:
            color = getattr(value, color.lower())
            return color8(color, 'bg' not in opts)
        except AttributeError:
            return color8(value.default, 'bg' not in opts)


class ANSI24ColorPalette(ColorPalette):
    def __format__(value, spec):
        color, *opts = spec.split(':')

        if color == 'endcolor':
            return value.endcolor

        try:
            color = getattr(value, color.lower())
            return color24(color, 'bg' not in opts)
        except AttributeError:
            return color24(value.default, 'bg' not in opts)


def color_string(string, fg=None, bg=None, extended=False):
    endcolor = '\x1B[m'
    prefix = ''
    suffix = ''

    mode = color24 if extended else color8

    if fg:
        prefix += mode(fg, foreground=True)
        suffix += endcolor

    if bg:
        prefix += mode(bg, foreground=False)
        suffix += endcolor

    return prefix + string + suffix


def color8(color, foreground=True):
    '''
    color text using either a color from xterm256
    or take an rgb triple and map it to xterm216
    '''
    selector = '38;5;' if foreground else '48;5;'

    if isinstance(color, tuple) and len(color) == 3:
        color = rgb_to_216(*color)

    assert isinstance(color, int)
    color = clamp(color, 0, 255)

    return f"\x1B[{selector}{color}m"


def color24(string, color, foreground=True):
    '''
    color text using a 24 bit rgb color
    '''
    assert isinstance(color, tuple) and len(color == 3)
    selector = '38;2;' if foreground else '48;2;'
    return f"\x1B[{selector}{color[0]};{color[1]};{color[2]}m"


def color_distance(R, G, B, r, g, b):
    '''
    L2 Norm in RGB color space
    '''
    return (R-r)**2 + (G-g)**2 + (B-b)**2


def nearest_cube_index(c):
    '''
    convert color in range 0-255 to xterm cube index
    '''
    if c < 75:
        c += 28

    return (c - 35) / 40


def rgb_to_216(r, g, b):
    corners = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)

    r_idx = nearest_cube_index(r)
    g_idx = nearest_cube_index(g)
    b_idx = nearest_cube_index(b)

    gray = (r + g + b) / 3 # not corrected for luminance, may be worthwhile to add
    gray_idx = 23 if gray > 238 else (gray - 3) / 10
    gray = 8 + (10 * gray_idx) # snap gray to ansi gray

    rgb_dist = color_distance(corners[r_idx], corners[g_idx], corners[b_idx], r, g, b)
    gray_dist = color_distance(gray, gray, gray, r, g, b)

    if gray_dist < rgb_dist:
        return 232 + gray_idx
    else:
        return 16 + (36 * r_idx) + (6 * g_idx) + b_idx
