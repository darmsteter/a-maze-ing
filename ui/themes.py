
from blessed import Terminal


EMOJI_THEMES = {
    "tree_garden": {
        "wall": lambda t: t.on_darkolivegreen('🌳'),  # 🍄🌸🌻
        "path": lambda t: t.darkolivegreen('  '),
        "start": lambda t: t.black('🐝'),
        "exit": lambda t: t.black('🌸'),
        "solution_path": lambda t: t.darkolivegreen('✨'),
        "pattern_42": lambda t: t.on_darkolivegreen('🍄')
    },
    "beach": {
        "wall": lambda t: t.on_color_rgb(238, 214, 175)('🌴'),
        "path": lambda t: t.on_color_rgb(238, 214, 175)('  '),
        "start": lambda t: t.bold_black_on_bright_yellow('🐶'),
        "exit": lambda t: t.bold_white_on_red('🏠'),
        "solution_path": lambda t: t.on_color_rgb(238, 214, 175)('🐾'),
        "pattern_42": lambda t: t.on_bright_cyan('☀️ ')
    },
    "halloween": {
        "wall": lambda t: t.on_black('💀'),  # 🧱☠️💀⚰🦴🧟🥀🩸🔥🦇🎃🍬🎪👻🧛🏻‍♀️🔮
        "path": lambda t: t.on_black('  '),
        "start": lambda t: t.on_black('🎪'),
        "exit": lambda t: t.on_black('🎃'),
        "solution_path": lambda t: t.on_black('🍬'),
        "pattern_42": lambda t: t.blink_on_black('🔥')
    },
    "snowman": {
        "wall": lambda t: t.on_lightcyan2('🥶'),  # 🧣🥕☃️ 🥶 🍫 ☕️🧊🛷🏠🐇
        "path": lambda t: t.on_lightcyan2('  '),
        "start": lambda t: t.on_paleturquoise4('🐇'),
        "exit": lambda t: t.on_color(153)('☃️ '),
        "solution_path": lambda t: t.on_lightcyan2('🥕'),
        "pattern_42": lambda t: t.on_darkslategray3('🧣')
    },
   
    "christmas": {
        "wall": lambda t: t.on_powderblue('🎄'),  # 🧱🎁🏠🎄🛷✨🫎🧸🦌🏡🏘️🛖🏠︎
        "path": lambda t: t.on_powderblue('  '),
        "start": lambda t: t.on_color(153)('🎅'),
        "exit": lambda t: t.on_color(153)('🏠'),
        "solution_path": lambda t: t.on_powderblue('🍪'),
        "pattern_42": lambda t: t.on_color(153)('🎁')
    },
}
# 🏠 🌼  

LINE_THEMES = {
    "green": {
        "wall": lambda t: t.springgreen4('██'),
        "path": lambda t: t.on_black('  '),
        "start": lambda t: t.bold_bright_yellow_on_black(' S'),
        "exit": lambda t: t.bold_red_on_black(' E'),
        "solution_path": lambda t: t.bold_white_on_black(' ★'),
        "pattern_42": lambda t: t.blink_bold_red_on_orange('42')
    },
    "pink": {
        "wall": lambda t: t.on_deeppink4('  '),
        "path": lambda t: t.on_plum1('  '),
        "start": lambda t: t.bold_red_on_lightyellow(' S'),
        "exit": lambda t: t.bold_yellow_on_red(' E'),
        "solution_path": lambda t: t.bold_black_on_plum1(' ★'),
        "pattern_42": lambda t: t.blink_maroon1_on_orchid1('██')
    },
    "purple": {
        "wall": lambda t: t.darkorchid4('▓▓'),
        "path": lambda t: t.on_mediumpurple2('  '),
        "start": lambda t: t.bold_red_on_white(' S'),
        "exit": lambda t: t.bold_white_on_red(' E'),
        "solution_path": lambda t: t.bold_gold_on_mediumpurple2(' ★'),
        "pattern_42": lambda t: t.blink_on_bright_yellow('  ')
    },
    "blue": {
        "wall": lambda t: t.on_darkblue('  '),
        "path": lambda t: t.on_lightblue('  '),
        "start": lambda t: t.bold_red_on_bright_yellow(' S'),
        "exit": lambda t: t.bold_bright_yellow_on_red(' E'),
        "solution_path": lambda t: t.bold_gray7_on_lightblue(' ★'),
        "pattern_42": lambda t: t.blink_on_magenta('  ')
    },
    "yellow": {
        "wall": lambda t: t.on_bright_yellow('  '),
        "path": lambda t: t.on_lemonchiffon2('  '),
        "start": lambda t: t.bold_bright_red_on_bright_blue(' S'),
        "exit": lambda t: t.bold_bright_yellow_on_red(' E'),
        "solution_path": lambda t: t.bold_black_on_lemonchiffon2(' ★'),
        "pattern_42": lambda t: t.blink_red_on_crimson('██')
    }
}
# ▒ ▒. ▓▓, █,


def get_tile(
    term: Terminal,
    tile_type: str,
    theme_name: str = "tree_garden",
    mode: str = "emoji"
) -> str:
    """Getting the grafic format from selected theme"""
    themes_dict = EMOJI_THEMES if mode == "emoji" else LINE_THEMES
    default_theme = "tree_garden" if mode == "emoji" else "green"

    theme = themes_dict.get(theme_name, themes_dict[default_theme])
    tile_formatter = theme.get(tile_type, lambda t: '  ')

    return tile_formatter(term)
