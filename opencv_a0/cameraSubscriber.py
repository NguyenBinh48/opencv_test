import rclpy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rclpy.node import Node

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')

        self.bridgeObj = CvBridge()

        self.topicName = 'camera_image'

        self.queueSize = 20
        
        self.subscription = self.create_subscription(Image, self.topicName, self.listener_callback, self.queueSize)
        self.subscription

    def listener_callback(self,ComingMessage):
        self.get_logger().info('The message is being received')
        Image = self.bridgeObj.imgmsg_to_cv2(ComingMessage)
        if Image is None:
            self.get_logger().info('Image is None')
        else:

            cv2.imshow('Camera Image', Image)
            cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    subscriberNode = CameraSubscriber()
    rclpy.spin(subscriberNode)
    subscriberNode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 