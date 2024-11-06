#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsClientNode(Node): 
    def __init__(self):
        super().__init__("add_two_ints_client") 
    
    def callback_add_two_ints_server(self,a,b):
        client = self.create_client(AddTwoInts,"add_two_ints")
        while not client.wait_for_service(2,0):
            self.get_logger().warn("WAITING FOR SERVER")
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        
        future = client.call_async(request)
        future.add_done_callback

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClientNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
