import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from evdev import InputDevice, categorize, ecodes  # Import required classes from evdev

class GamepadNode(Node):
    def __init__(self):
        super().__init__('gamepad_node')
        self.publisher = self.create_publisher(String, 'gamepad_events', 10)

    def publish_event(self, message):
        msg = String()
        msg.data = message
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = GamepadNode()

    # Replace with the correct path to your gamepad device
    device = InputDevice('/dev/input/event7')

    try:
        for event in device.read_loop():
            if event.type in [ecodes.EV_ABS, ecodes.EV_KEY]:
                node.publish_event(str(categorize(event)))
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
