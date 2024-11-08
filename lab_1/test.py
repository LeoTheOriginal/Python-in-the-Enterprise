import unittest
from unittest.mock import patch
from task import Car, Environment, Action


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.environment = Environment()

    def test_start_the_engine(self):
        with self.assertLogs(level='INFO') as log:
            self.environment.start_the_engine()
            self.assertIn("Starting the engine...", log.output[0])
            self.assertIn("Engine started. Car is ready to drive.", log.output[1])

    def test_drive_sets_on_the_road(self):
        self.environment.drive()
        self.assertTrue(self.environment.on_the_road)
        self.assertGreater(self.environment.speed, 0)

    def test_accelerate_increases_speed(self):
        self.environment.accelerate(2)
        self.assertGreater(self.environment.speed, 0)

    def test_brake_reduces_speed(self):
        self.environment.speed = 50
        self.environment.brake(1)
        self.assertLess(self.environment.speed, 50)

    def test_highway_sets_on_the_highway(self):
        self.environment.highway()
        self.assertTrue(self.environment.on_the_highway)
        self.assertGreater(self.environment.speed, 0)

    def test_overtake_increases_speed_highway(self):
        self.environment.on_the_highway = True
        self.environment.overtake()
        self.assertEqual(self.environment.speed, Environment.OVERTAKE_SPEED_HIGHWAY)

    def test_truck_decreases_speed_highway(self):
        self.environment.on_the_highway = True
        self.environment.truck()
        self.assertEqual(self.environment.speed, Environment.TRUCK_SPEED_HIGHWAY)

    def test_stop_resets_speed_and_on_the_road(self):
        self.environment.stop()
        self.assertFalse(self.environment.on_the_road)
        self.assertEqual(self.environment.speed, 0)


class TestCar(unittest.TestCase):
    def setUp(self):
        self.environment = Environment()
        self.car = Car(self.environment)

    def test_send_action_start_the_engine(self):
        with patch.object(Environment, 'start_the_engine') as mock_start:
            self.car.send_action(Action('start the engine'))
            mock_start.assert_called_once()

    def test_stop_sets_running_false(self):
        self.car.stop()
        self.assertFalse(self.car.running)

if __name__ == '__main__':
    unittest.main()
