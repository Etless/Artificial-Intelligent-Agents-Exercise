import time
import robot_dog as robot


# Hunger and bladder percentage can be altered when creating dog
robot1 = robot.RobotDog()

print("Robot Dog is starting")
robot1.start_robot()
time.sleep(120)

print("Robot Dog is stopping")
robot1.stop_robot()

