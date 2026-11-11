import random

from pico2d import get_canvas_height, get_canvas_width

from bird import Bird, DRAW_HEIGHT, DRAW_WIDTH, FRAME_COUNT


BIRD_COUNT = 10


def create_flock(rng=None):
    """위치·방향·속도를 생성 시 한 번 정해 개체별 비행을 유지한다."""
    rng = rng if rng is not None else random
    width, height = get_canvas_width(), get_canvas_height()
    left, right = DRAW_WIDTH / 2, width - DRAW_WIDTH / 2
    bottom = max(180, height * 0.38)
    top = height - DRAW_HEIGHT / 2 - 12
    heights = list(range(BIRD_COUNT))
    directions = [-1] * (BIRD_COUNT // 2) + [1] * (BIRD_COUNT - BIRD_COUNT // 2)
    rng.shuffle(heights)
    rng.shuffle(directions)
    return [
        Bird(left + (right - left) * (index + rng.uniform(0.2, 0.8)) / BIRD_COUNT,
             bottom + (top - bottom) *
             (heights[index] + rng.uniform(0.2, 0.8)) / BIRD_COUNT,
             initial_frame=(index + rng.random()) * FRAME_COUNT / BIRD_COUNT,
             direction=directions[index],
             speed=rng.uniform(120, 190))
        for index in range(BIRD_COUNT)
    ]
