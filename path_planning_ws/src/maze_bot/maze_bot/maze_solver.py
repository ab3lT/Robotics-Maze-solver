import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
from math import pi,cos,sin

from .bot_localization import bot_localizer
from .bot_mapping import bot_mapper
from .bot_pathplanning import bot_pathplanner
from .bot_motionplanning import bot_motionplanner

from nav_msgs.msg import Odometry

import numpy as np
from numpy import interp

from .utilities import Debugging
from . import config

class maze_solver(Node):

    def __init__(self):
        
        super().__init__("maze_solving_node")
        
        self.velocity_publisher = self.create_publisher(Twist,'/cmd_vel',10)
        self.videofeed_subscriber = self.create_subscription(Image,'/upper_camera/image_raw',self.get_video_feed_cb,10)
        
        # Visualizing what the robot sees by subscribing to bot_camera/Image_raw
        self.bot_subscriber = self.create_subscription(Image,'/Botcamera/image_raw',self.process_data_bot,10)

        self.timer = self.create_timer(0.2, self.maze_solving)
        self.bridge = CvBridge()
        self.vel_msg = Twist()
        
        # Creating objects for each stage of the robot navigation
        self.bot_localizer = bot_localizer()
        self.bot_mapper = bot_mapper()
        self.bot_pathplanner = bot_pathplanner()
        self.bot_motionplanner = bot_motionplanner()

        # Subscrbing to receive the robot pose in simulation
        self.pose_subscriber = self.create_subscription(Odometry,'/odom',self.bot_motionplanner.get_pose,10)
        self.vel_subscriber = self.create_subscription(Odometry,'/odom',self.get_bot_speed,10)
        self.bot_speed = 0
        self.bot_turning = 0

        self.sat_view = np.zeros((100,100))

        self.debugging = Debugging()

    def get_video_feed_cb(self,data):
        frame = self.bridge.imgmsg_to_cv2(data,'bgr8')
        self.sat_view = frame
    
    def process_data_bot(self, data):
        self.bot_view = self.bridge.imgmsg_to_cv2(data,'bgr8') # performing conversion

    def maze_solving(self):
        
        self.debugging.setDebugParameters()

        # Creating frame to display current robot state to user        
        frame_disp = self.sat_view.copy()
        
        # [Stage 1: Localization] Localizing robot at each iteration        
        self.bot_localizer.localize_bot(self.sat_view, frame_disp)

        # [Stage 2: Mapping] (Not Implemented Yet)
        self.bot_mapper.graphify(self.bot_localizer.maze_og)

        # [Stage 3: PathPlanning] (Not Implemented Yet)
        start = self.bot_mapper.Graph.start
        end = self.bot_mapper.Graph.end
        maze = self.bot_mapper.maze

        self.bot_pathplanner.find_path_nd_display(self.bot_mapper.Graph.graph, start, end, maze,method="dijisktra")
        self.bot_pathplanner.find_path_nd_display(self.bot_mapper.Graph.graph, start, end, maze,method="a_star")
        
        # [Stage 4: MotionPlanning] (Not Implemented Yet)
        bot_loc = self.bot_localizer.loc_car
        path = self.bot_pathplanner.path_to_goal
        self.bot_motionplanner.nav_path(bot_loc, path, self.vel_msg, self.velocity_publisher)
        
        cv2.imshow("Maze (Live)", frame_disp)
        cv2.waitKey(1)

def main(args =None):
    rclpy.init()
    node_obj =maze_solver()
    rclpy.spin(node_obj)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
