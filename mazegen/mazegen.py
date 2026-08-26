import os
import mlx

TILE_SIZE = 32

colors = {
    '1': 0x00FF00,  # Perete: Verde
    '0': 0x000000,  # Cale: Negru
    'S': 0xFFFF00,  # Start: Galben
    'E': 0xFF0000   # Iesire: Rosu
}


def close_program(param=None):
    """Callback function to terminate the program immediately."""
    os._exit(0)


def handle_key(keycode, param=None):
    """Handle ESC key to exit. (ESC key is 65307 on Linux / 53 on MacOs)."""
    if keycode in (65307, 53):
        os._exit(0)
    return 0


def draw_block(buf, size_line, pixel_bytes, start_x, start_y, dimension, color):
    """Draw a single block pixel by pixel directly into the image buffer."""
    r = (color >> 16) & 0xFF
    g = (color >> 8) & 0xFF
    b = color & 0xFF

    for y in range(start_y, start_y + dimension):
        row_offset = y * size_line
        for x in range(start_x, start_x + dimension):
            offset = row_offset + x * pixel_bytes
            buf[offset] = b
            buf[offset + 1] = g
            buf[offset + 2] = r
            buf[offset + 3] = 255   # <-- opac, nu 0 (transparent)


def render_maze(param):
    """Redraw the pre-built image onto the window (cheap blit)."""
    m, mlx_ptr, win_ptr, img_ptr = param
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
    return 0


def grafic_initialization(maze_map):
    """Initialize MinilibX window and register event loops."""
    lines_num = len(maze_map)
    columns_num = len(maze_map[0])

    window_width = columns_num * TILE_SIZE
    window_hight = lines_num * TILE_SIZE

    m = mlx.Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, window_width, window_hight, "A_maze_ing")

    img_ptr = m.mlx_new_image(mlx_ptr, window_width, window_hight)
    buf, bpp, size_line, img_format = m.mlx_get_data_addr(img_ptr)
    pixel_bytes = bpp // 8

    # Popularea imaginii o singura data la inceput
    for y in range(lines_num):
        for x in range(columns_num):
            position = maze_map[y][x]
            pos_x = x * TILE_SIZE
            pos_y = y * TILE_SIZE
            block_color = colors.get(position, 0x000000)
            draw_block(buf, size_line, pixel_bytes, pos_x, pos_y, TILE_SIZE, block_color)

    # Afisarea initiala pe fereastra
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

    # Hook-uri si evenimente
    m.mlx_loop_hook(win_ptr, render_maze, (m, mlx_ptr, win_ptr, img_ptr))
    m.mlx_hook(win_ptr, 17, 0, close_program, None)
    m.mlx_hook(win_ptr, 2, 1, handle_key, None)

    m.mlx_loop(mlx_ptr)


# Testing draw_block issue

# import mlx

# m = mlx.Mlx()
# mlx_ptr = m.mlx_init()
# win_ptr = m.mlx_new_window(mlx_ptr, 100, 100, "debug")
# img_ptr = m.mlx_new_image(mlx_ptr, 100, 100)

# buf, bpp, size_line, img_format = m.mlx_get_data_addr(img_ptr)

# print("bpp:", bpp)
# print("size_line:", size_line)
# print("format:", img_format)
# print("len(buf):", len(buf))

# pixel_bytes = bpp // 8
# print("pixel_bytes:", pixel_bytes)

# # Umple tot buffer-ul cu ALB pur (255,255,255) si alpha maxim, ca sa fie
# # imposibil sa nu se vada daca scrierea in buffer chiar ajunge pe ecran.
# #
# for i in range(len(buf)):
#     buf[i] = 255

# print("primii 20 bytes dupa umplere:", list(buf[:20]))

# m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
# m.mlx_loop(mlx_ptr)