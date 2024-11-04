#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class NumberCounterNode(Node):

    def __init__(self):
        self.a = 0
        super().__init__("number_counter")
        self.subscriber_ = self.create_subscription(Int64,"number",self.callback_number,10)
        self.publisher_ = self.create_publisher(Int64,"number_count",10)
        self.timer = self.create_timer(0.5,self.publish_number_count)
        self.get_logger().info("number_counter opened")


    def callback_number(self,msg):
        self.get_logger().info(f"Received data: {msg.data} (int64)")
        self.a += 1

    def publish_number_count(self):
        msg = Int64()
        msg.data = self.a
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
