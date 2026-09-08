
EMOJI_THEMES = {
    "tree_garden": {
        "wall": lambda t: t.on_lightgreen('🌳'),
        "path": lambda t: t.on_black('🟫'),
        "start": lambda t: t.on_yellow('🏠'),
        "exit": lambda t: t.on_white('🚪'),
        "pattern_42": lambda t: t.on_yellow('🧱')
    },
    "snowman": {
        "wall": lambda t: t.on_lightblue('🧸ྀི'),
        "path": lambda t: t.on_lightblue('  '),
        "start": lambda t: t.on_blue('⛇ '),
        "exit": lambda t: t.on_red('❄️ '),
    },
    "beach": {
        "wall": lambda t: t.on_lightyellow('🌴'),
        "path": lambda t: t.on_brown('🏻'),
        "start": lambda t: t.on_green('𖠋 '),
        "exit": lambda t: t.on_red('🏆'),
    },
    "christmas": {
        "wall": lambda t: t.on_lightblue('🎄'),  # 🧱
        "path": lambda t: t.on_lightblue('⬜'),
        "start": lambda t: t.on_blue('🎅'),
        "exit": lambda t: t.on_white('🎁'),
    },
    "halloween": {
        "wall": lambda t: t.on_orange('🍁'),  # 🧱
        "path": lambda t: t.on_orange('  '),
        "start": lambda t: t.on_blue('🎅'),
        "exit": lambda t: t.on_white('🎁'),
    },
}

LINE_THEMES = {
    "classic_pink": {
        "wall": lambda t: t.on_pink('▓▓'),
        "path": lambda t: t.on_black('  '),
        "start": lambda t: t.on_yellow(' S'),
        "exit": lambda t: t.on_red(' E'),
    },
    "cyber_blue": {
        "wall": lambda t: t.on_blue('▓▓'),
        "path": lambda t: t.on_purple('▒▒'),
        "start": lambda t: t.on_yellow(' S'),
        "exit": lambda t: t.on_red(' Ⓔ '),
    },
}
