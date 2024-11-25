import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from evdev import InputDevice, ecodes  # Import only required classes

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
            # Check for axis (joystick movement) or button events
            if event.type == ecodes.EV_ABS:  # Axis (e.g., joystick movement)
                axis_name = ecodes.ABS.get(event.code, f"Unknown Axis ({event.code})")
                axis_value = event.value
                message = f"Axis: {axis_name}, Value: {axis_value}"
                node.publish_event(message)
                print(message)

            elif event.type == ecodes.EV_KEY:  # Buttons (e.g., A, B, X, Y)
                button_name = ecodes.BTN.get(event.code, f"Unknown Button ({event.code})")
                button_state = "Pressed" if event.value == 1 else "Released"
                message = f"Button: {button_name}, States: {button_state}, Value: {event.value}"
                node.publish_event(message)
                print(message)

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
