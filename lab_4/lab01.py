#!/usr/bin/env python3


#
# Plane simulator.
# Write a code in python that simulates the tilt correction of the plane (angle between plane wings and earth).
# The program should print out current orientation, and applied tilt correction.
# (Tilt is "Roll" in this diagram https://upload.wikimedia.org/wikipedia/commons/c/c1/Yaw_Axis_Corrected.svg)
# The program should run in infinite loop, until user breaks the loop.
# Assume that plane orientation in every new simulation step is changing with random angle with gaussian distribution
# (the planes is experiencing "turbulence").
# Hint: "random.gauss(0, 2*rate_of_turbulence)"
# With every simulation step the orentation should be corrected, correction should be applied and printed out.
# Try to expand your implementation as best as you can.
# Think of as many features as you can, and try implementing them.
#
# Try to expand your implementation as best as you can.
# Think of as many features as you can, and try implementing them.
# Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
# Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
# The goal of this task is for you to SHOW YOUR BEST python programming skills.
# Impress everyone with your skills, show off with your code.
#
# Your program must be runnable with command "python task.py".
# Show some usecases of your library in the code (print some things)
# Delete these comments before commit!
#
# Good luck.


# klasa samolot 5 metod,
# generatory,
# wywołać każdą funkcje,
# multi processing

import random
import logging

logger = logging.getLogger('task')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class Flight:
    def __init__(self, rate_of_turbulence, stabilization_level, plane):
        """
        Initializes a new Flight instance.

        Args:
            rate_of_turbulence (float): The initial rate of turbulence affecting the plane's movement.
            stabilization_level (float): The initial level of stabilization to counteract the turbulence.
            plane (Plane): An instance of the Plane class representing the aircraft being simulated.
        """
        self.rate_of_turbulence = rate_of_turbulence
        self.stabilization_level = stabilization_level
        self.plane = plane

    def change_rate_of_turbulence(self, change):
        """
        Adjusts the rate of turbulence affecting the plane.

        Args:
            change (float): The new rate of turbulence to be set.
        """
        logger.info(f"Rate of correction is changed to {change}")
        self.rate_of_turbulence = change

    def change_stabilization_level(self, change):
        """
        Adjusts the stabilization level used to counteract the turbulence.

        Args:
            change (float): The new stabilization level to be set.
        """
        logger.info(f"Stabilization level is changed to {change}")
        self.stabilization_level = change

    def turbulence(self):
        """
        Simulates the effect of turbulence on the plane by randomly adjusting its Pitch, Roll, and Yaw.
        """
        logger.info("\nThe plane is having turbulences")
        self.plane.Pitch += random.gauss(0, 2 * self.rate_of_turbulence)
        self.plane.Roll += random.gauss(0, 2 * self.rate_of_turbulence)
        self.plane.Yaw += random.gauss(0, 2 * self.rate_of_turbulence)

    def stabilization(self):
        """
        Applies stabilization corrections to the plane's Pitch, Roll, and Yaw based on the stabilization level.
        """
        if self.stabilization_level > 1:
            self.stabilization_level = 1 / self.stabilization_level
        logger.info(f'The plane was corrected by {self.plane.Pitch * (1 - self.stabilization_level):.2f} ,'
                    f'{self.plane.Roll * (1 - self.stabilization_level):.2f} ,'
                    f'{self.plane.Yaw * (1 - self.stabilization_level):.2f}')
        self.plane.Pitch *= (1 - self.stabilization_level)
        self.plane.Roll *= (1 - self.stabilization_level)
        self.plane.Yaw *= (1 - self.stabilization_level)

    def falling(self):
        """
        Simulates a stop of an engine and tilt of a beak of a plane to the ground.
        """
        logger.info("The plane is falling down!!!!!\n")
        self.plane.Pitch = -90

    def flight_simulator(self):
        """
        Runs the main loop for the flight simulation, allowing the user to choose various actions.
        """
        logger.info("Starting the flight\n")
        while True:
            logger.info(f'{self.plane}\n')
            task = input(
                "Choose an action for a plane: (stabalize, turbulence, change_turbulence, change_level_of_stability,"
                " fall, test_flight, exit)")
            if task == 'stabalize':
                self.stabilization()
            elif task == 'turbulence':
                self.turbulence()
            elif task == 'change_turbulence':
                change = float(input("Enter the turbulence level: "))
                self.change_rate_of_turbulence(change)
            elif task == 'change_level_of_stability':
                change = float(input("Enter the correction level (0-1): "))
                self.change_stabilization_level(change)
            elif task == 'fall':
                self.falling()
            elif task == 'test_flight':
                correction = float(input("Enter the correction level (0-1): "))
                turbulence = float(input("Enter the turbulence level: "))
                self.test_flight(turbulence, correction)

            elif task == 'exit':
                logger.info('Thanks for flying with Python airlines :D')
                break
            else:
                logger.info('This command do not exists')

    def test_flight(self, rate_of_turbulence, stabilization_level):
        """
        Shows functions that can be used on a flight.

        Args:
            rate_of_turbulence (float): The new rate of turbulence to be set.
            stabilization_level (float): The new stabilization level to be set.
        """
        self.turbulence()
        self.stabilization()
        logger.info(self.plane)
        self.change_rate_of_turbulence(rate_of_turbulence)
        self.change_stabilization_level(stabilization_level)
        self.falling()
        logger.info(self.plane)
        self.stabilization()
        self.stabilization()
        logger.info(self.plane)


class Plane:
    def __init__(self, pitch, roll, yaw):
        """
        Initializes a new instance of the Plane class.

        Args:
            pitch (float): The initial pitch angle of the plane.
            roll (float): The initial roll angle of the plane.
            yaw (float): The initial yaw angle of the plane.
        """
        self.Pitch = pitch
        self.Roll = roll
        self.Yaw = yaw

    def __str__(self):
        """
        Returns a string representation of the current angles of the plane.

        Returns:
            str: A string showing the current pitch, roll, and yaw of the plane.
        """
        self.display_angle()
        return f"Now the plane has Pitch= {self.Pitch:.2f}, Roll={self.Roll:.2f} and Yaw={self.Yaw:.2f}"

    def display_angle(self):
        """
        Normalizes the angles of the plane to be within the range [-180, 180) degrees.
        This method modifies the Pitch, Roll, and Yaw attributes directly.
        """
        self.Pitch = ((self.Pitch + 180) % 360) - 180
        self.Roll = ((self.Roll + 180) % 360) - 180
        self.Yaw = ((self.Yaw + 180) % 360) - 180


if __name__ == "__main__":
    a = Plane(10., 20., 30.)
    print(a)
    test = Flight(15, 0.5, a)
    test.test_flight(30, 0.6)
    test.flight_simulator()
