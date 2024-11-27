#!/usr/bin/env python3


# Your task is to get the code from your friend
# copy the code of your friend, preferably as separate files to this repository
# Test all of the methods in their code, or at least 10 unittest tests (that make sense).
# Your test must be runnable with the command `python -m unittest task`
# Write down the address of your friends repo here:
#
# Imported from: https://github.com/agh-pite2024-win/group3-task1-Carrot5161/blob/main/task.py
#

# change the name of OTHER_CODE, to the code that you imported cd ../lab01

import unittest
from unittest.mock import patch
from lab01 import Flight, Plane


class TestPlaneSimulation(unittest.TestCase):

    def setUp(self):
        self.plane = Plane(0, 0, 0)
        self.flight = Flight(10, 0.5, self.plane)

    def test_initialization(self):
        self.assertEqual(self.plane.Pitch, 0)
        self.assertEqual(self.plane.Roll, 0)
        self.assertEqual(self.plane.Yaw, 0)

    def test_turbulence(self):
        initial_pitch = self.plane.Pitch
        initial_roll = self.plane.Roll
        initial_yaw = self.plane.Yaw

        with patch('random.gauss', return_value=5):
            self.flight.turbulence()

        self.assertNotEqual(self.plane.Pitch, initial_pitch)
        self.assertNotEqual(self.plane.Roll, initial_roll)
        self.assertNotEqual(self.plane.Yaw, initial_yaw)

    def test_stabilization(self):
        self.plane.Pitch = 50
        self.plane.Roll = 50
        self.plane.Yaw = 50
        self.flight.stabilization()

        self.assertAlmostEqual(self.plane.Pitch, 25)
        self.assertAlmostEqual(self.plane.Roll, 25)
        self.assertAlmostEqual(self.plane.Yaw, 25)

    def test_change_rate_of_turbulence(self):
        self.flight.change_rate_of_turbulence(20)
        self.assertEqual(self.flight.rate_of_turbulence, 20)

    def test_change_stabilization_level(self):
        self.flight.change_stabilization_level(0.8)
        self.assertEqual(self.flight.stabilization_level, 0.8)

    def test_falling(self):
        self.flight.falling()
        self.assertEqual(self.plane.Pitch, -90)

    def test_plane_display_angle(self):
        self.plane.Pitch = 370
        self.plane.Roll = -190
        self.plane.Yaw = 720
        self.plane.display_angle()

        self.assertEqual(self.plane.Pitch, 10)
        self.assertEqual(self.plane.Roll, 170)
        self.assertEqual(self.plane.Yaw, 0)

    @patch('lab01.logger')
    def test_flight_simulator_exit(self, mock_logger):
        with patch('builtins.input', side_effect=['exit']):
            self.flight.flight_simulator()

        mock_logger.info.assert_any_call('Thanks for flying with Python airlines :D')

    @patch('lab01.logger')
    def test_flight_simulator_stabilize(self, mock_logger):
        with patch('builtins.input', side_effect=['stabalize', 'exit']):
            self.flight.flight_simulator()

        # Sprawdź, czy komunikat stabilizacji się pojawił
        self.assertTrue(any('The plane was corrected by' in call[0][0] for call in mock_logger.info.call_args_list))

    def test_test_flight(self):
        with patch('random.gauss', return_value=5):
            self.flight.test_flight(20, 0.7)

        self.assertEqual(self.flight.rate_of_turbulence, 20)
        self.assertAlmostEqual(self.flight.stabilization_level, 0.7)


if __name__ == '__main__':
    unittest.main()
