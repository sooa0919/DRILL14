from pico2d import load_image


SHEET_COLUMNS = 5
SHEET_ROWS = 3
FRAME_COUNT = 14
DRAW_WIDTH = 92
DRAW_HEIGHT = 84


class Bird:
    image = None

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0.0

    def source_rect(self):
        # 파일은 위쪽부터 행 순서로 배치되고 pico2d는 아래쪽이 원점이다.
        index = int(self.frame) % FRAME_COUNT
        column, row = index % SHEET_COLUMNS, index // SHEET_COLUMNS
        left = column * self.image.w // SHEET_COLUMNS
        right = (column + 1) * self.image.w // SHEET_COLUMNS
        top = row * self.image.h // SHEET_ROWS
        bottom = (row + 1) * self.image.h // SHEET_ROWS
        return left, self.image.h - bottom, right - left, bottom - top

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(*self.source_rect(), self.x, self.y,
                             DRAW_WIDTH, DRAW_HEIGHT)
