from pico2d import get_canvas_width, load_image

import game_framework


SHEET_COLUMNS = 5
SHEET_ROWS = 3
FRAME_COUNT = 14
DRAW_WIDTH = 92
DRAW_HEIGHT = 84
FRAMES_PER_SECOND = 14.0
FLIGHT_SPEED_PPS = 160.0


class Bird:
    image = None

    def __init__(self, x, y, initial_frame=0):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = float(initial_frame) % FRAME_COUNT
        self.left = DRAW_WIDTH / 2
        self.right = get_canvas_width() - DRAW_WIDTH / 2
        self.x = max(self.left, min(self.right, x))
        self.travel = self.x - self.left
        self.direction = 1

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
        self.frame = (self.frame + FRAMES_PER_SECOND *
                      game_framework.frame_time) % FRAME_COUNT
        span = self.right - self.left
        if span <= 0:
            self.x = get_canvas_width() / 2
            return
        # 왕복 거리로 나눈 나머지는 여러 번 경계를 넘는 긴 프레임도 처리한다.
        self.travel = (self.travel + FLIGHT_SPEED_PPS *
                       game_framework.frame_time) % (2 * span)
        self.direction = 1 if self.travel < span else -1
        self.x = self.left + (self.travel if self.direction == 1
                              else 2 * span - self.travel)

    def draw(self):
        self.image.clip_draw(*self.source_rect(), self.x, self.y,
                             DRAW_WIDTH, DRAW_HEIGHT)
