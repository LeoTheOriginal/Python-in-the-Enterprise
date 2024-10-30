import time
import random
import logging
import multiprocessing


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class Action:
    def __init__(self, name: str, duration: int = 0) -> None:
        self.name = name
        self.duration = duration


class Environment:
    MAX_SPEED_HIGHWAY = 140
    MAX_SPEED_ROAD = 50
    OVERTAKE_SPEED_HIGHWAY = 160
    OVERTAKE_SPEED_ROAD = 70
    TRUCK_SPEED_HIGHWAY = 90
    TRUCK_SPEED_ROAD = 50

    def __init__(self) -> None:
        self.speed: int = 0
        self.wheel_angle: int = 0
        self.on_the_road: bool = False
        self.on_the_highway: bool = False

    def handle_action(self, action: Action) -> None:
        if action.name == 'start the engine':
            self.start_the_engine()
        elif action.name == 'drive':
            self.drive()
        elif action.name == 'turn':
            self.turn()
        elif action.name == 'accelerate':
            self.accelerate(action.duration if action.duration != 0 else 3)
        elif action.name == 'brake':
            self.brake(action.duration if action.duration != 0 else 2)
        elif action.name == 'obstacle':
            self.avoid_obstacle()
        elif action.name == 'highway':
            self.highway()
        elif action.name == 'exit highway':
            self.exit_highway()
        elif action.name == 'overtake':
            self.overtake()
        elif action.name == 'truck':
            self.truck()
        elif action.name == 'status':
            self.status()
        elif action.name == 'stop':
            self.stop()
        else:
            self.log_message("Unknown action")

    @staticmethod
    def log_message(message: str) -> None:
        logging.info(message)

    def start_the_engine(self=None) -> None:
        self.log_message("Starting the engine...")
        time.sleep(1)
        self.log_message("Engine started. Car is ready to drive.")
        time.sleep(1)
        self.log_message("Please enter a 'drive' command to start driving.")

    def drive(self) -> None:
        self.log_message("Driving...")
        self.on_the_road = True
        time.sleep(1)
        self.accelerate(5)
        time.sleep(1)
        self.log_message("Car is on the road.")

    def turn(self) -> None:
        angle = random.gauss(0, 15)  # mean=0, stddev=15
        for _ in range(3):
            self.wheel_angle = angle
            time.sleep(0.1)
            self.log_message(f"Turning... Wheel angle: {self.wheel_angle}°")
            angle -= 7.50 if angle >= 0 else -7.50
        self.wheel_angle = 0

    def accelerate(self, duration: int = 3) -> None:
        def accelerate_generator():
            for _ in range(duration):
                if self.on_the_highway:
                    yield from self._increase_speed(self.MAX_SPEED_HIGHWAY)
                else:
                    yield from self._increase_speed(self.MAX_SPEED_ROAD)

        for speed in accelerate_generator():
            time.sleep(1)
            self.log_message(f"Accelerating... Speed: {speed} km/h")

    def _increase_speed(self, max_speed: int) -> None:
        def speed_generator():
            while self.speed < max_speed:
                self.speed += 10
                yield self.speed

        yield from speed_generator()

    def brake(self, duration: int = 2) -> None:
        def brake_generator():
            for _ in range(duration):
                if self.speed > 0:
                    self.speed -= 10
                    yield self.speed
                else:
                    break
        for speed in brake_generator():
            self.log_message(f"Braking... Speed: {speed} km/h")
            time.sleep(1)
        time.sleep(1)

    def avoid_obstacle(self) -> None:
        self.log_message("Obstacle detected. Avoiding the obstacle...")
        time.sleep(1)
        self.brake(1)
        time.sleep(1)
        self.turn()
        self.log_message(f"Car's speed decreasing to {self.speed}")

    def highway(self) -> None:
        self.log_message("Entering the highway...")
        self.on_the_highway = True
        time.sleep(1)
        self.log_message("Car is on the highway.")
        time.sleep(1)
        self.accelerate(10)
        self.wheel_angle = 0

    def exit_highway(self) -> None:
        self.log_message("Exiting the highway...")
        time.sleep(1)
        self.brake(1)
        self.log_message("Car is on the road.")
        time.sleep(1)
        self.on_the_highway = False

    def overtake(self) -> None:
        if self.on_the_highway:
            self.log_message(f"Overtaking... Speed set to {self.OVERTAKE_SPEED_HIGHWAY} km/h.")
            self.speed = self.OVERTAKE_SPEED_HIGHWAY
        else:
            self.log_message(f"Overtaking... Speed set to {self.OVERTAKE_SPEED_ROAD} km/h.")
            self.speed = self.OVERTAKE_SPEED_ROAD

    def truck(self) -> None:
        if self.on_the_highway:
            self.log_message(f"Truck ahead! Slowing down to {self.TRUCK_SPEED_HIGHWAY} km/h.")
            self.speed = self.TRUCK_SPEED_HIGHWAY
        else:
            self.log_message(f"Truck ahead! Slowing down to {self.TRUCK_SPEED_ROAD} km/h.")
            self.speed = self.TRUCK_SPEED_ROAD

    def status(self) -> None:
        self.log_message(f"Car's current status: speed = {self.speed}, wheel angle = {self.wheel_angle}°")
        if self.on_the_highway:
            self.log_message("Car is on the highway.")
        elif self.on_the_road:
            self.log_message("Car is on the road.")
        else:
            self.log_message("Car is not on the road.")

    def stop(self) -> None:
        self.log_message("Stopping the car...")
        time.sleep(1)
        self.on_the_road = False
        self.speed = 0
        self.log_message("Car has stopped.")
        time.sleep(1)


class Car:
    def __init__(self, environment: Environment) -> None:
        self.environment = environment
        self.running = True

    def send_action(self, action: Action) -> None:
        self.environment.handle_action(action)

    def stop(self) -> None:
        self.running = False

    def __del__(self) -> None:
        self.stop()


def action_generator():
    while True:
        command = input("Enter a command: ").strip().lower()
        if command == 'exit':
            logging.info("Exiting the car simulation...")
            time.sleep(1)
            break
        yield Action(command)


def handle_action_in_process(action: Action, car: Car) -> None:
    car.send_action(action)


if __name__ == '__main__':
    logging.info("Starting car simulation...")
    time.sleep(1)
    logging.info("Car simulation started.")
    time.sleep(1)

    environment = Environment()
    car1 = Car(environment)
    car1.running = True

    action_gen = action_generator()
    with multiprocessing.Pool() as pool:
        pool.apply_async(car1.send_action, (Action('start the engine'),))
        for action in action_gen:
            pool.apply_async(handle_action_in_process, args=(action, car1))
            if not car1.running:
                break

    logging.info("Car simulation ended.")
