import constants


from utilities import load_image, draw_image, draw_polygon, draw_rect_center, draw_ellipse_centered, draw_text, \
    play_music, play_sfx, draw_button


def tile_reset():
    first_cell_center_x = constants.BOARD_CENTER_X - (constants.NUM_COLS // 2 * constants.SPACING)
    first_cell_center_y = constants.BOARD_CENTER_Y - (constants.NUM_ROWS // 2 * constants.SPACING)
    for j in range(constants.NUM_ROWS):
        for i in range(constants.NUM_COLS):
            Tile.board_tiles.append(
                Tile(first_cell_center_x + constants.SPACING * i, first_cell_center_y + constants.SPACING * j,
                      constants.CELL_SIZE, constants.SPACING, j, i))


class Tile:

    total_tiles = 0
    board_tiles = []
    def __init__(self, xpos, ypos, size, spacing, row, col):
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.row = row
        self.col = col

    def draw(self, window) -> None:
        color = constants.COLOR_BLACK
        draw_rect_center(
            window,
            (self.xpos, self.ypos),
            (constants.CELL_SIZE, constants.CELL_SIZE),
            color,
            0,
            1)
        draw_rect_center(
            window,
            (self.xpos, self.ypos),
            (constants.CELL_SIZE, constants.CELL_SIZE),
            color,
            0)

    def hitbox(self):
        top = self.ypos - self.size/2
        bottom = self.ypos + self.size/2
        left = self.xpos - self.size/2
        right = self.xpos + self.size/2
        return {"Left" : left, "Top" : top, "Right" : right, "Bottom" : bottom}

    def animate(self):
        pass

