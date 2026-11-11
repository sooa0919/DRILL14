from pico2d import get_canvas_height, get_canvas_width

from bird import Bird, FRAME_COUNT


BIRD_COUNT = 10


def create_flock():
    """하늘 두 줄에 다섯 마리씩 배치하고 날갯짓 위상을 분산한다."""
    width, height = get_canvas_width(), get_canvas_height()
    return [
        Bird(width * (0.20 + (index % 5) * 0.12),
             height * (0.70 + (index // 5) * 0.18),
             initial_frame=index * FRAME_COUNT / BIRD_COUNT)
        for index in range(BIRD_COUNT)
    ]
