import cv2

import rclpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rclpy.node import Node


class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')
        
        self.cameraDevice = 2
        self.camera = cv2.VideoCapture(self.cameraDevice, cv2.CAP_V4L2)    #cv2.CAP_V4L2  is used for Linux
        self.bridgeObj = CvBridge()
        
        self.topicName = 'camera_image'

        self.queueSize = 20

        self.publisher = self.create_publisher(Image, self.topicName, self.queueSize)

        FPS0 = 0.01666666666 # 60 FPS
        FPS1 = 0.02 # 50 FPS
        FPS2 = 0.03333333333 # 30 FPS
        FPS3 = 0.05 # 20 FPS

        self.timerControl= FPS0
        self.timer = self.create_timer(self.timerControl, self.timer_callback)

        self.i = 0 
    
    def timer_callback(self):
        success, frame = self.camera.read()
        size1 = (820,640)
        size2 = (640,480)

        frame = cv2.resize(frame, (size1), interpolation=cv2.INTER_CUBIC)
        frame = cv2.flip(frame, 1)

        if success == True:
            ROS2Image = self.bridgeObj.cv2_to_imgmsg(frame)
            self.publisher.publish(ROS2Image)

        self.get_logger().info('Publishing image %d' % self.i)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    publisherNode = CameraPublisher()
    rclpy.spin(publisherNode)
    publisherNode.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()    
