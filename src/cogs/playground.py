from colormap import rgb2hex

from src.cogs.etc.config import colors

colors_ = {}

for k, v in colors.items():
    colors_[k] = rgb2hex(v[0], v[1], v[2]).replace('#', '0x')

print(colors_)
