
from blessed import Terminal


EMOJI_THEMES = {
    "tree_garden": {
        "wall": lambda t: t.on_lightgreen('🌳'),
        "path": lambda t: t.on_lightgreen('  '),
        "start": lambda t: t.on_yellow('🚩'),
        "exit": lambda t: t.on_red('🏁'),
        "solution_path": lambda t: t.on_lightgreen('🐾'),
        "pattern_42": lambda t: t.blink('💠')
    },
    "snowman": {
        "wall": lambda t: t.on_lightblue('🧸ྀི'),
        "path": lambda t: t.on_lightblue('  '),
        "start": lambda t: t.bold_black_on_yellow('⛇ '),
        "exit": lambda t: t.bold_white_on_red('❄️ '),
        "pattern_42": lambda t: t.on_orange('🧱')
    },
    "beach": {
        "wall": lambda t: t.on_lightyellow('🌴'),
        "path": lambda t: t.on_brown('🏻'),
        "start": lambda t: t.bold_black_on_yellow('𖠋 '),
        "exit": lambda t: t.bold_white_on_red('🏆'),
        "pattern_42": lambda t: t.on_orange('🧱')
    },
    "christmas": {
        "wall": lambda t: t.on_lightblue('🎄'),  # 🧱
        "path": lambda t: t.on_lightblue('⬜'),
        "start": lambda t: t.on_blue('🎅'),
        "exit": lambda t: t.bold_white_on_red('🎁'),
        "pattern_42": lambda t: t.on_orange('🧱')
    },
    "halloween": {
        "wall": lambda t: t.on_orange('🍁'),  # 🧱
        "path": lambda t: t.on_orange('  '),
        "start": lambda t: t.bold_black_on_yellow('🎅'),
        "exit": lambda t: t.bold_white_on_red('🎁'),
        "pattern_42": lambda t: t.on_orange('🧱')
    },
}

LINE_THEMES = {
    "classic_pink": {
        "wall": lambda t: t.on_green('▒▒'),
        "path": lambda t: t.on_black('  '),
        "start": lambda t: t.bold_black_on_yellow(' S'),
        "exit": lambda t: t.bold_white_on_red(' E'),
        "solution_path": lambda t: t.white_on_black('○'),
        "pattern_42": lambda t: t.on_orange('  ')
    },
    "cyber_blue": {
        "wall": lambda t: t.on_blue('▓▓'),
        "path": lambda t: t.on_purple('  '),
        "start": lambda t: t.bold_black_on_yellow(' S'),
        "exit": lambda t: t.bold_white_on_red(' E'),
        "pattern_42": lambda t: t.on_yellow('██')
    },
    "box_drawing": {
        "wall": lambda t: t.on_green('██'),
        "path": lambda t: '  ',
        "start": lambda t: t.bold_black_on_yellow(' S'),
        "exit": lambda t: t.bold_white_on_red(' E'),
        "pattern_42": lambda t: t.on_orange('  ')
    }
}


def get_tile(
    term: Terminal,
    tile_type: str,
    theme_name: str = "tree_garden",
    mode: str = "emoji"
) -> str:
    """Getting the grafic format from selected theme"""
    themes_dict = EMOJI_THEMES if mode == "emoji" else LINE_THEMES
    default_theme = "tree_garden" if mode == "emoji" else "classic_pink"

    theme = themes_dict.get(theme_name, themes_dict[default_theme])
    tile_formatter = theme.get(tile_type, lambda t: '  ')

    return tile_formatter(term)

# ▒ ▒. ▓▓, █,
# 🏠
