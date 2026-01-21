import threading
import random
import time


class RobotDog(threading.Thread):
    def __init__(self, hunger_per = 10, bladder_per = 4):
        threading.Thread.__init__(self)
        self.interrupt = False

        # Shared memory variables
        self.pos = (0,0) # Some position of the robot
        self.hunger_per = hunger_per   # Hunger%  1/i
        self.bladder_per = bladder_per # Bladder% 1/i

        self.move = (0, 0)
        self.bladder = False
        self.hunger = False


        # Lock used to halt operation of other threads
        self.lock = threading.Lock()

        # Create thread of each class
        self.t0 = threading.Thread(target=self.action)
        self.t1 = threading.Thread(target=self.roam)
        self.t2 = threading.Thread(target=self.eat)
        self.t3 = threading.Thread(target=self.relieve)


    def start_robot(self):
        self.t0.start()
        self.t1.start()
        self.t2.start()
        self.t3.start()

    def stop_robot(self):
        self.interrupt = True
        self.t0.join()
        self.t1.join()
        self.t2.join()
        self.t3.join()


    # The actuator that actually does what is needed
    def action(self):
        while not self.interrupt:
            self.lock.acquire()  # Lock thread

            # Priority is handled by the if-else statements
            # where only one action is performed each loop

            if self.bladder: # Highest priority
                print("Relieving myself")
                time.sleep(2) # Time it takes to relieve itself
                self.bladder = False

            elif self.hunger: # Medium priority
                print("Eating food")
                time.sleep(2)  # Time it takes to eat
                self.hunger = False

            elif not self.move == (0, 0):
                self.pos = (self.pos[0] + self.move[0], self.pos[1] + self.move[1])
                print("I'm roaming to ", self.pos)
                time.sleep(1)  # Time it takes to move
                self.move = (0, 0)

            self.lock.release() # Unlock thread
            time.sleep(2)

    # All different states for robot

    # Due to the nonspecification of there needing to be a specific area
    # for the robot to relive itself, the relive function will purely be visual
    def relieve(self):
        while not self.interrupt:
            self.lock.acquire() # Lock thread
            if random.randint(1,self.bladder_per + 1) == 1:
                print("Bladder full!")
                self.bladder = True

            self.lock.release() # Unlock thread
            time.sleep(3)

    # Due to the nonspecification of there needing to be a food item
    # available, the eat function will purely be visual
    def eat(self):
        while not self.interrupt:
            self.lock.acquire() # Lock thread
            if random.randint(1,self.hunger_per + 1) == 1:
                print("I'm hungry!")
                self.hunger = True

            self.lock.release() # Unlock thread
            time.sleep(3)

    # Robot can walk in 8 directions or choose to not move
    def roam(self):
        while not self.interrupt:
            self.lock.acquire() # Lock thread

            _x = random.randint(-1,1) # random number between -1 to 1
            _y = random.randint(-1,1) # ^^^
            self.move = (_x, _y)

            self.lock.release()  # Unlock thread
            time.sleep(3)