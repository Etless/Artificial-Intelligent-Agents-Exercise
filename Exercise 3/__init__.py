import time
import robot_dog as robot


robot = robot.RobotDog()

print("Robot Dog is starting")
robot.start_robot()
time.sleep(120)

print("Robot Dog is stopping")
robot.stop_robot()
