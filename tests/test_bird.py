import unittest
import random
from unittest.mock import Mock, patch

import bird
import game_framework
import flock
import game_world
import play_mode


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

    def test_reflection_preserves_remaining_distance(self):
        subject = bird.Bird(1550, 400)
        game_framework.frame_time = 0.1
        subject.update()
        self.assertAlmostEqual(subject.x, 1542)
        self.assertEqual(subject.direction, -1)

    def test_exact_endpoints_face_inward(self):
        subject = bird.Bird(46, 400)
        game_framework.frame_time = (1554 - 46) / bird.FLIGHT_SPEED_PPS
        subject.update()
        self.assertEqual((subject.x, subject.direction), (1554, -1))
        subject.update()
        self.assertEqual((subject.x, subject.direction), (46, 1))

    def test_large_delta_spans_multiple_round_trips(self):
        subject = bird.Bird(200, 400)
        span = subject.right - subject.left
        game_framework.frame_time = (10 * 2 * span + 200) / bird.FLIGHT_SPEED_PPS
        subject.update()
        self.assertAlmostEqual(subject.x, 400)
        self.assertEqual(subject.direction, 1)

    def test_left_start_moves_left_without_initial_jump(self):
        subject = bird.Bird(800, 400, direction=-1, speed=125)
        self.assertEqual((subject.x, subject.direction), (800, -1))
        game_framework.frame_time = 0
        subject.update()
        self.assertEqual((subject.x, subject.direction), (800, -1))
        game_framework.frame_time = 0.2
        subject.update()
        self.assertAlmostEqual(subject.x, 775)
        self.assertEqual(subject.direction, -1)

    def test_same_duration_at_different_frame_rates(self):
        results = []
        for fps in (30, 60, 144):
            subject = bird.Bird(1200, 400, 2)
            game_framework.frame_time = 1 / fps
            for _ in range(fps * 25):
                subject.update()
                self.assertTrue(subject.left <= subject.x <= subject.right)
            results.append((subject.x, subject.frame, subject.direction))
        for x, frame, direction in results:
            self.assertAlmostEqual(x, results[0][0])
            self.assertAlmostEqual(frame, results[0][1])
            self.assertEqual(direction, results[0][2])

    def test_ten_distinct_birds_inside_sky(self):
        with patch('flock.get_canvas_width', return_value=1600), \
                patch('flock.get_canvas_height', return_value=600):
            birds = flock.create_flock(random.Random(42))
        self.assertEqual(len(birds), 10)
        self.assertEqual(len({(b.x, b.y) for b in birds}), 10)
        self.assertEqual(len({b.frame for b in birds}), 10)
        self.assertEqual(len({b.y for b in birds}), 10)
        self.assertEqual([b.direction for b in birds].count(-1), 5)
        self.assertEqual([b.direction for b in birds].count(1), 5)
        self.assertEqual(len({b.speed for b in birds}), 10)
        for subject in birds:
            self.assertTrue(120 <= subject.speed <= 190)
            self.assertTrue(subject.left <= subject.x <= subject.right)
            self.assertGreaterEqual(subject.y - bird.DRAW_HEIGHT / 2, 60)
            self.assertLessEqual(subject.y + bird.DRAW_HEIGHT / 2, 600)

    def test_mode_registers_and_cleans_up_flock_on_restart(self):
        saved_world = game_world.world
        saved_boy = play_mode.boy
        game_world.world = [[], [], []]
        try:
            with patch('play_mode.Boy'), patch('play_mode.Grass'), \
                    patch('flock.get_canvas_width', return_value=1600), \
                    patch('flock.get_canvas_height', return_value=600):
                for _ in range(2):
                    play_mode.init()
                    self.assertEqual(sum(isinstance(o, bird.Bird)
                                         for o in game_world.world[1]), 10)
                    game_framework.frame_time = 0.25
                    play_mode.update()
                    play_mode.finish()
                    self.assertTrue(all(not layer for layer in game_world.world))
        finally:
            game_world.world = saved_world
            play_mode.boy = saved_boy


if __name__ == '__main__':
    unittest.main()
