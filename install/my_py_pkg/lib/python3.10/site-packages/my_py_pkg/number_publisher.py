#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
import random



class NumberPublisherNode(Node):
    
    def __init__(self):
        super().__init__("number_publisher")
        self.publisher_ = self.create_publisher(Int64, "number", 10)
        self.timer_ = self.create_timer(0.5,self.publish_numbers)
        self.get_logger().info("number publisher has started")

    def publish_numbers(self):
        
        number = Int64()
        number.data = random.randint(0,100)
        self.publisher_.publish(number)
        


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
