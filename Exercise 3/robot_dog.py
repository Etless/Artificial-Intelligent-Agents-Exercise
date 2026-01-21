import threading

# Shared memory variables
status


# All different states for robot

def relieve(self):
    print("Bladder full, relieving myself")
    pass


def eat(self):
    print("Im hungry, eating")
    pass


def roam(self):
    pass

def RoboDog():
    interrupt = False
    t1 = threading.Thread(target=roam, args=(lambda: interrupt))
    t2 = threading.Thread(target=eat, args=(lambda: interrupt))
    t3 = threading.Thread(target=relieve, args=(lambda: interrupt))