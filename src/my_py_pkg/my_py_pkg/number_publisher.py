#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
import random



class NumberPublisherNode(Node):
    
    def __init__(self):
        super().__init__("number_publisher")
        self.declare_parameter("number_to_publish",2)
        self.declare_parameter("publish_freq" , 1.0)
        
        #self.number_ = random.randint(0,100)
        self.number_ = self.get_parameter("number_to_publish").value
        self.publish_freq_ = self.get_parameter("publish_freq").value
        self.publisher_ = self.create_publisher(Int64, "number", 10)
        self.timer_ = self.create_timer(
            1.0 / self.publish_freq_ ,self.publish_numbers)
        self.get_logger().info("number publisher has started")

    def publish_numbers(self):
        
        msg = Int64()
        msg.data = self.number_
        self.publisher_.publish(msg)
        


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
