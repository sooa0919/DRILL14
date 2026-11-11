import unittest
from unittest.mock import Mock, patch

import bird
import game_framework


class BirdTests(unittest.TestCase):
    def setUp(self):
        self.old_image = bird.Bird.image
        self.old_time = game_framework.frame_time
        bird.Bird.image = None
        self.image = Mock(w=918, h=506)
        loader = patch('bird.load_image', return_value=self.image)
        width = patch('bird.get_canvas_width', return_value=1600)
        self.loader = loader.start()
        width.start()
        self.addCleanup(loader.stop)
        self.addCleanup(width.stop)
        self.addCleanup(self.restore_globals)

    def restore_globals(self):
        bird.Bird.image = self.old_image
        game_framework.frame_time = self.old_time

    def test_shared_image_loaded_once(self):
        bird.Bird(200, 400)
        bird.Bird(500, 500)
        self.loader.assert_called_once_with('bird_animation.png')

    def test_source_rect_covers_only_fourteen_valid_cells(self):
        subject = bird.Bird(200, 400)
        cells = []
        for frame in range(14):
            subject.frame = frame
            x, y, w, h = subject.source_rect()
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + w, 918)
            self.assertLessEqual(y + h, 506)
            cells.append((x, y, w, h))
        self.assertEqual(len(set(cells)), 14)
        self.assertEqual(cells[0], (0, 338, 183, 168))
        self.assertEqual(cells[-1], (550, 0, 184, 169))
        subject.frame = 14
        self.assertEqual(subject.source_rect(), cells[0])

    def test_wing_cycle_uses_elapsed_seconds(self):
        subject = bird.Bird(200, 400, initial_frame=3)
        game_framework.frame_time = 0.5
        subject.update()
        self.assertEqual(subject.frame, 10)
        subject.update()
        self.assertEqual(subject.frame, 3)

    def test_draw_flips_only_when_facing_left(self):
        subject = bird.Bird(200, 400)
        for direction, flip in [(1, ''), (-1, 'h')]:
            subject.direction = direction
            subject.draw()
            self.assertEqual(self.image.clip_composite_draw.call_args.args[5], flip)


if __name__ == '__main__':
    unittest.main()
