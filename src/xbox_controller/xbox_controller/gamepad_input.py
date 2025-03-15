import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from evdev import InputDevice, ecodes, list_devices


class XboxArmController(Node):
    def __init__(self, device_path: str):
        super().__init__('xbox_arm_controller')
        self.trajectory_pub = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)

        self.device_path = device_path
        self.device = self._initialize_device()

        self.joint_angles = {
            'joint_1': 0.0,
            'joint_2': 0.0,
            'joint_3': 0.0,
            'joint_4': 0.0,
            'joint_5': 0.0,
            'joint_6': 0.0,
        }

        # Axis mapping to joints
        self.axis_joint_map = {
            0: 'joint_1',  # Left stick X
            1: 'joint_2',  # Left stick Y
            3: 'joint_3',  # Right stick X
            4: 'joint_4',  # Right stick Y
        }

        # Button control for additional joints
        self.button_joint_map = {
            317: ('joint_5', -1),  # L Stick Click
            318: ('joint_5', 1),   # R Stick Click
        }

        self.step = 0.05  # radians per event
        self.deadzone = 5000  # joystick deadzone threshold

        self.axis_values = {0: 0, 1: 0, 3: 0, 4: 0}

    def _initialize_device(self):
        try:
            device = InputDevice(self.device_path)
            self.get_logger().info(f"Connected to controller: {device.name} at {self.device_path}")
            return device
        except Exception as e:
            self.get_logger().error(f"Failed to connect to controller: {e}")
            rclpy.shutdown()
            exit(1)

    def publish_joint_trajectory(self):
        msg = JointTrajectory()
        msg.joint_names = list(self.joint_angles.keys())
        point = JointTrajectoryPoint()
        point.positions = list(self.joint_angles.values())
        point.time_from_start.sec = 1
        msg.points.append(point)
        self.trajectory_pub.publish(msg)
        self.get_logger().info(f"🚀 Trajectory sent: {self.joint_angles}")

    def read_gamepad_events(self):
        self.get_logger().info("🎮 Xbox controller active. Move sticks to control joints. Press START to execute. Ctrl+C to exit.")
        try:
            for event in self.device.read_loop():
                if event.type == ecodes.EV_ABS:  # Joystick movement
                    self._handle_axis_motion(event.code, event.value)
                elif event.type == ecodes.EV_KEY and event.value == 1:  # Button press
                    if event.code == 315:  # Start button
                        self.get_logger().info("▶️ Start button pressed. Executing trajectory.")
                        self.publish_joint_trajectory()
                    else:
                        self._handle_button_press(event.code)
                        self._log_joint_angles()
        except KeyboardInterrupt:
            self.get_logger().info("🛑 Xbox control node stopped.")
        except Exception as e:
            self.get_logger().error(f"Error: {e}")

    def _handle_axis_motion(self, code, value):
        if code in self.axis_joint_map:
            joint = self.axis_joint_map[code]
            normalized_value = value / 32768.0  # Normalize to [-1, 1]
            if abs(value) < self.deadzone:  # Deadzone
                normalized_value = 0.0
            delta = normalized_value * self.step
            self.joint_angles[joint] += delta
            self.joint_angles[joint] = max(min(self.joint_angles[joint], 3.14), -3.14)  # Limit to [-pi, pi]
            self.get_logger().info(f"{joint} moved to {self.joint_angles[joint]:.2f} rad")
            self.publish_joint_trajectory()  # Continuous update

    def _handle_button_press(self, code):
        joint_action = self.button_joint_map.get(code)
        if joint_action:
            joint_name, direction = joint_action
            self.joint_angles[joint_name] += self.step * direction
            self.get_logger().info(f"{joint_name} adjusted to {self.joint_angles[joint_name]:.2f} rad")
        else:
            self.get_logger().info(f"⚠️ Unknown button code {code}")

    def _log_joint_angles(self):
        angles_str = ', '.join([f"{k}: {v:.2f}" for k, v in self.joint_angles.items()])
        self.get_logger().info(f"🦾 Current target angles: {angles_str}")


def list_input_devices():
    devices = list_devices()
    return devices if devices else []


def main():
    rclpy.init()
    devices = list_input_devices()
    if not devices:
        print("❌ No input devices found. Connect Xbox controller.")
        return

    print("\nAvailable devices:")
    for idx, dev_path in enumerate(devices):
        dev = InputDevice(dev_path)
        print(f"[{idx}] {dev_path} - {dev.name}")

    default_device_path = devices[0]
    print(f"\n✅ Using device: {default_device_path}")

    node = XboxArmController(device_path=default_device_path)
    node.read_gamepad_events()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
