import random


class Car:
    def __init__(self):
        self.wheel_angle = 0
        self.speed = 100
        self.on_the_road = True

    def go_right(self):
        self.speed = 50
        self.wheel_angle = -45

    def go_left(self):
        self.speed = 50
        self.wheel_angle = 45

    def go_straight(self, time):
        if time % 2 == 0:
            self.speed = 100
            self.wheel_angle = 0

    def act(self, event):
        if event == 'obstacle on right':
            self.go_left()
        elif event == 'obstacle on left':
            self.go_right()
        elif event == 'obstacle in front':
            if random.randint(0, 1):
                self.go_right()
            else:
                self.go_left()


time = 1
i = 0
car1 = Car()
event = ['obstacle on right', 'no obstacle', 'obstacle on left', 'no obstacle', 'obstacle in front']

if __name__ == '__main__':
    while (True):
        car1.act(event[i])
        car1.go_straight(time)
        print(event[i], car1.wheel_angle, car1.speed)
        time += 1
        if time % 3 == 0:
            i += 1
        if len(event) <= i:
            i = 0




