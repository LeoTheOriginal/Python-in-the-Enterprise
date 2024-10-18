# Write a module that will simulate autonomic car.
# The simulation is event based, an example:
# car1 = Car()
# car1.act(event)
# print(car1.wheel_angle, car1.speed)
# where event can be anything you want, i.e. :
# `('obstacle', 10)` where `10` is a duration (time) of the event.
##The program should:
# - act on the event
# - print out current steering wheel angle, and speed
# - run in infinite loop
# - until user breaks the loop

#The level of realism in simulation is of your choice, but more sophisticated solutions are better.
#If you can think of any other features, you can add them.
#Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
#Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
#The goal of this task is for you to SHOW YOUR BEST python programming skills.
#Impress everyone with your skills, show off with your code.
#
#Your program must be runnable with command "python task.py".
#Show some usecases of your library in the code (print some things)
#
#When you are done upload this code to github repository.
#
#Delete these comments before commit!
#Good luck.

class Car:
    def __init__(self):
        self.speed = 0
        self.wheel_angle = ''

    def act(self, event):
        if event == 'starting':
            self.wheel_angle = 'forward'
            while self.speed != 50:
                self.speed += 10
                print("Car's speed increasing: ", self.speed)
            self.event_status(event)
        elif event == 'obstacle':
            if self.speed - 0.1 * self.speed > 0:
                self.speed -= self.speed * 0.1
                self.wheel_angle = 'forward'
            self.event_status(event)
        elif event == 'motorway':
            self.speed = 100
            self.wheel_angle = 'forward'
            self.event_status(event)
        elif event == 'overtaking':
            self.speed = 70
            self.wheel_angle = 'changing'
            self.event_status(event)
        elif event == 'truck':
            self.speed = 50
            self.wheel_angle = 'forward'
            self.event_status(event)

    def status(self):
        print("Car's speed: ", self.speed, "wheel angle: ", self.wheel_angle)

    def event_status(self, event):
        print("Type of event: ", event, "car's speed: ", self.speed, "wheel angle: ", self.wheel_angle)

    def stop(self):
        self.speed = 0
        self.wheel_angle = ''
        print("Car's speed: ", self.speed, "wheel angle: ", self.wheel_angle)


car1 = Car()
print(car1.speed)
print(car1.wheel_angle)
