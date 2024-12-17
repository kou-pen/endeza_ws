import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import cv2
from cv2 import aruco
import numpy as np
import time
import math

constant = 720 * 5.15

class CameraMove(Node):
    def __init__(self):
        super().__init__('camera_move')
        self.Framerate = 60
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters()
        self.markID = 1
        self.detector = aruco.ArucoDetector(self.dictionary, self.parameters)
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        if not self.cap.isOpened():
            print("WebCamera is not found")
            exit()
        print('CameraMove node has been created')
        
        self.front_power_pub = self.create_publisher(Float64, 'front_power', 10)
        self.side_power_pub = self.create_publisher(Float64, 'side_power', 10)
        
        self.timer = self.create_timer(1/self.Framerate, self.timer_callback)
        
    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejectedCandidates = self.detector.detectMarkers(gray)
        
        if self.markID in np.ravel(ids):
            index = np.where(ids == self.markID)[0][0]
            cornerUL = corners[index][0][0]
            cornerUR = corners[index][0][1]
            cornerBR = corners[index][0][2]
            cornerBL = corners[index][0][3]
            center = [(cornerUL[0] + cornerBR[0]) * 0.5, (cornerUL[1] + cornerBR[1]) * 0.5]
            
            side_x = (cornerUL[0] - cornerUR[0])
            side_y = (cornerUL[1] - cornerUR[1])
            front_x = (cornerUL[0] - cornerBL[0])
            front_y = (cornerUL[1] - cornerBL[1])
            
            side_power = side_x / constant
            front_power = front_y / constant
            
            # TODO: Calculate the power of the front and side motors
            
            self.front_power_pub.publish(Float64(data=front_power))
            self.side_power_pub.publish(Float64(data=side_power))
            

def main(args=None):
    rclpy.init(args=args)
    camera_move = CameraMove()
    
    rclpy.spin(camera_move)
    
    camera_move.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
    
    
        
    
        
    
    