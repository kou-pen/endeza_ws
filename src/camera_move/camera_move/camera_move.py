import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from cv2 import aruco
import numpy as np
import time
import math

constant = 720 * 5.15

class CameraMove(Node):
    def __init__(self):
        super().__init__('camera_move')
        self.Framerate = 15
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters()
        self.markID = 1
        self.detector = aruco.ArucoDetector(self.dictionary, self.parameters)
        self.bridge = CvBridge()
        
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        if not self.cap.isOpened():
            print("WebCamera is not found")
            exit()
        print('CameraMove node has been created')
        
        self.front_power_pub = self.create_publisher(Float64, 'front_power', 10)
        self.rotate_power_pub = self.create_publisher(Float64, 'rotate_power', 10)
        self.image_pub = self.create_publisher(Image, 'image', 10)
        
        self.timer = self.create_timer(1/self.Framerate, self.timer_callback)
        
    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejectedCandidates = self.detector.detectMarkers(gray)
        # frame = aruco.drawDetectedMarkers(frame, corners, ids)
        
        # img = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        # self.image_pub.publish(img)
        
        if self.markID in np.ravel(ids):
            index = np.where(ids == self.markID)[0][0]
            cornerUL = corners[index][0][0]
            # cornerUR = corners[index][0][1]
            cornerBR = corners[index][0][2]
            # cornerBL = corners[index][0][3]
            center = [(cornerUL[0] + cornerBR[0]) * 0.5, (cornerUL[1] + cornerBR[1]) * 0.5]
            
            # side_x = (cornerUL[0] - cornerUR[0])
            # side_y = (cornerUL[1] - cornerUR[1])
            # front_x = (cornerUL[0] - cornerBL[0])
            # front_y = (cornerUL[1] - cornerBL[1])
            
            # rotate_power = side_x / constant
            # front_power = front_y / constant
            # print(rotate_power, front_power)
            
            # TODO: Calculate the power of the front and side motors
            
            # self.front_power_pub.publish(Float64(data=float(front_power)))
            # self.rotate_power_pub.publish(Float64(data=float(rotate_power)))
            
            # from_center_x = (center[0] - 360) if center[0] < 360 else (360 - center[0])
            from_center_x = center[0] - 360
            print(from_center_x, center[0])
            
            self.rotate_power_pub.publish(Float64(data=float(from_center_x / 20)))
            

def main(args=None):
    rclpy.init(args=args)
    camera_move = CameraMove()
    
    rclpy.spin(camera_move)
    
    camera_move.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
    
    
        
    
        
    
    
