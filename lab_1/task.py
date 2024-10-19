import time
import random


class Car:
    def __init__(self):
        self.speed = 0
        self.wheel_angle = 0
        self.simulator_running = True
        self.running = False
        self.on_the_road = False
        self.on_the_highway = False
        self.events_handled = 0

    def act(self, event):
        match event:
            case 'start the engine':
                self.start_the_engine()
            case 'drive':
                self.drive()
            case 'turn':
                self.turn()
            case 'accelerate':
                self.accelerate()
            case 'brake':
                self.brake()
            case 'obstacle':
                self.avoid_obstacle()
            case 'highway':
                self.highway()
            case 'exit highway':
                self.exit_highway()
            case 'overtake':
                self.overtake()
            case 'truck':
                self.truck()
            case 'status':
                self.status()
            case 'stop':
                self.stop()
            case 'exit':
                self.exit()
            case 'help':
                print("Available commands: start the engine, drive, turn, accelerate, brake, obstacle, highway, "
                      "exit highway, overtake, truck, status, stop, exit, help")
            case _:
                print("Unknown command")

        self.events_handled += 1

    def not_running(self):
        if not self.running:
            print("Car's engine is not running. Please start the engine first.")
        return not self.running

    def not_on_the_road(self):
        if not self.on_the_road:
            print("Car is not on the road. Please enter a \"drive\" command first.")
        return not self.on_the_road

    def start_the_engine(self):
        if self.not_running():
            print("Starting the engine...")
            time.sleep(1)
            print("Engine started. Car is ready to drive.")
            time.sleep(1)
            print("Please enter a \"drive\" command to start driving.")
            self.running = True
        elif self.on_the_road or self.on_the_highway:
            print("Engine is already running. You can continue driving.")
        else:
            print("Engine is already running. Please enter a \"drive\" command to start driving.")

    def drive(self):
        if self.not_running():
            return
        print("Driving...")
        time.sleep(1)
        self.accelerate(5)
        time.sleep(1)
        print("Car is on the road.")
        self.on_the_road = True

    def turn(self):
        if self.not_running():
            return
        angle = random.randint(-30, 30)
        for _ in range(3):
            self.wheel_angle = angle
            time.sleep(0.1)
            print(f"Turning... Wheel angle: {self.wheel_angle}°")
            angle -= 7.50 if angle >= 0 else -7.50
        self.wheel_angle = 0  # Reset to forward after the turn

    def accelerate(self, duration=3):
        if self.not_running():
            return
        if self.not_on_the_road():
            return
        for _ in range(duration):
            if self.on_the_highway:
                if self.speed < 140:  # Max speed
                    self.speed += 10
                    time.sleep(0.1)
                    print(f"Accelerating... Speed: {self.speed} km/h")
            else:
                if self.speed < 50:
                    self.speed += 10
                    time.sleep(0.1)
                    print(f"Accelerating... Speed: {self.speed} km/h")

    def brake(self, duration=2):
        if self.running is False or self.speed == 0:
            print("Car is already stopped.")
            return
        for _ in range(duration):
            if self.speed > 0:
                self.speed -= 10
            else:
                self.speed = 0
            time.sleep(0.1)
            print(f"Braking... Speed: {self.speed} km/h")

    def avoid_obstacle(self):
        if self.not_running():
            return
        if self.speed == 0:
            print("Car is already stopped.")
            return
        print("Obstacle detected. Avoiding the obstacle...")
        time.sleep(1)
        self.brake(1)
        time.sleep(1)
        self.turn()
        print("Car's speed decreasing to", self.speed)

    def highway(self):
        if self.not_running():
            return
        if not self.on_the_road:
            print("Car is not on the road. Please enter a \"drive\" command first.")
            return
        if self.on_the_highway:
            print("Car is already on the highway.")
            return

        print("Entering the highway...")
        time.sleep(1)
        print("Car is on the highway.")
        time.sleep(1)
        self.accelerate(10)
        self.wheel_angle = 0
        self.on_the_highway = True

    def exit_highway(self):
        if self.not_running():
            return
        if not self.on_the_highway:
            print("Car is not on the highway.")
            return
        print("Exiting the highway...")
        time.sleep(1)
        self.brake(9)
        print("Car is on the road.")
        time.sleep(1)
        self.on_the_highway = False

    def overtake(self):
        if self.not_running():
            return
        if self.not_on_the_road():
            return
        if self.on_the_highway:
            print("Overtaking... Speed set to 160 km/h.")
            self.speed = 160
        else:
            print("Overtaking... Speed set to 70 km/h.")
            self.speed = 70

    def truck(self):
        if self.not_running():
            return
        if self.not_on_the_road():
            print("Car is not on the road. Please enter a \"drive\" command first.")
            return
        if self.on_the_highway:
            print("Truck ahead! Slowing down to 100 km/h.")
            self.speed = 100
        else:
            self.speed = 50
            print("Truck ahead! Slowing down to 50 km/h.")

    def status(self):
        print("Car's current status: speed =", self.speed, ", wheel angle =", self.wheel_angle, "°, Engine =", "running" if self.running else "not running")
        if self.on_the_highway:
            print("Car is on the highway.")
        elif self.on_the_road:
            print("Car is on the road.")
        else:
            print("Car is not on the road.")

    def stop(self):
        if self.running is False:
            print("Car is already stopped.")
            return
        if self.on_the_highway:
            self.exit_highway()
        print("Stopping the car...")
        time.sleep(1)
        self.running = False
        self.on_the_road = False
        self.speed = 0
        print("Car has stopped.")
        time.sleep(1)

    def exit(self):
        print("Exiting the car simulation...")
        time.sleep(1)
        self.running = False
        self.simulator_running = False
        print("Car simulation ended.")
        time.sleep(1)


# Rozpoczęcie symulacji
print("Starting car simulation...")
time.sleep(1)
print("Car simulation started.")
time.sleep(1)

# Główna pętla sterująca samochodem
car1 = Car()
while car1.simulator_running:
    command = input("Enter a command: ").strip().lower()
    car1.act(command)

print(f"Simulation ended after handling {car1.events_handled} events.")
