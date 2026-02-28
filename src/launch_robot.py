#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
launch_robot.py
---------------
Lanza un Robot que escucha la cola saimazoom_robot_queue.
"""

from saimazoom_lib.robot import Robot

def main():
    robot = Robot(robot_id=1, prob_no_encontrar=0.1, config_file="config/server.conf")
    robot.start()
    robot.start_consuming()
    robot.stop()

if __name__ == "__main__":
    main()