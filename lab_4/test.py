import unittest
from unittest.mock import patch
from car import Car  # Zakładamy, że klasa Car jest w pliku car.py


class TestCar(unittest.TestCase):
    def setUp(self):
        self.car = Car()

    def test_initial_conditions(self):
        # Testuje warunki początkowe
        self.assertEqual(self.car.wheel_angle, 0)
        self.assertEqual(self.car.speed, 100)
        self.assertTrue(self.car.on_the_road)

    def test_go_right(self):
        # Testuje funkcję skrętu w prawo
        self.car.go_right()
        self.assertEqual(self.car.wheel_angle, -45)
        self.assertEqual(self.car.speed, 50)

    def test_go_left(self):
        # Testuje funkcję skrętu w lewo
        self.car.go_left()
        self.assertEqual(self.car.wheel_angle, 45)
        self.assertEqual(self.car.speed, 50)

    def test_go_straight_even_time(self):
        # Testuje funkcję jazdy prosto przy parzystym czasie
        self.car.go_straight(2)
        self.assertEqual(self.car.wheel_angle, 0)
        self.assertEqual(self.car.speed, 100)

    def test_go_straight_odd_time(self):
        # Testuje funkcję jazdy prosto przy nieparzystym czasie (sprawdza, czy nie zmienia prędkości i kąta)
        self.car.speed = 50
        self.car.wheel_angle = 10
        self.car.go_straight(3)
        self.assertEqual(self.car.wheel_angle, 10)
        self.assertEqual(self.car.speed, 50)

    @patch('random.randint', return_value=0)
    def test_act_obstacle_in_front_right(self, mock_randint):
        # Testuje zdarzenie przeszkody z przodu (wybierając skręt w prawo)
        self.car.act('obstacle in front')
        self.assertEqual(self.car.wheel_angle, -45)
        self.assertEqual(self.car.speed, 50)

    @patch('random.randint', return_value=1)
    def test_act_obstacle_in_front_left(self, mock_randint):
        # Testuje zdarzenie przeszkody z przodu (wybierając skręt w lewo)
        self.car.act('obstacle in front')
        self.assertEqual(self.car.wheel_angle, 45)
        self.assertEqual(self.car.speed, 50)

    def test_act_obstacle_on_right(self):
        # Testuje zdarzenie przeszkody po prawej stronie (powinien skręcić w lewo)
        self.car.act('obstacle on right')
        self.assertEqual(self.car.wheel_angle, 45)
        self.assertEqual(self.car.speed, 50)

    def test_act_obstacle_on_left(self):
        # Testuje zdarzenie przeszkody po lewej stronie (powinien skręcić w prawo)
        self.car.act('obstacle on left')
        self.assertEqual(self.car.wheel_angle, -45)
        self.assertEqual(self.car.speed, 50)

    def test_act_no_obstacle(self):
        # Testuje sytuację braku przeszkody (powinien pozostać bez zmian)
        initial_speed = self.car.speed
        initial_wheel_angle = self.car.wheel_angle
        self.car.act('no obstacle')
        self.assertEqual(self.car.wheel_angle, initial_wheel_angle)
        self.assertEqual(self.car.speed, initial_speed)


if __name__ == '__main__':
    unittest.main()
