#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, MagneticField
import serial
import json

class ScunGunBridge(Node):
    def __init__(self):
        super().__init__('scungun_bridge')
        
        # Publishers
        self.imu_pub = self.create_publisher(Imu, 'imu/data', 10)
        self.mag_pub = self.create_publisher(MagneticField, 'imu/mag', 10)
        
        # Connect to Pico
        try:
            # Serial port might be /dev/ttyACM0 or /dev/ttyACM1
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
            self.get_logger().info("--- SCUN-GUN LINK ESTABLISHED ---")
        except Exception as e:
            self.get_logger().error(f"SERIAL ERROR: {e}")
            exit()

        # Timer runs at ~100Hz to match the Pico's output
        self.create_timer(0.01, self.telemetry_callback)

    def telemetry_callback(self):
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                data = json.loads(line)
                
                msg = Imu()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "imu_link"

                # 1. Orientation + Placeholder Covariance
                msg.orientation.x = data['qx']
                msg.orientation.y = data['qy']
                msg.orientation.z = data['qz']
                msg.orientation.w = data['qw']
                # Diagonal matrix: [roll, pitch, yaw]
                msg.orientation_covariance = [
                    0.001, 0.0, 0.0,
                    0.0, 0.001, 0.0,
                    0.0, 0.0, 0.001
                ]

                # 2. Angular Velocity + Placeholder Covariance
                msg.angular_velocity.x = data['gx']
                msg.angular_velocity.y = data['gy']
                msg.angular_velocity.z = data['gz']
                msg.angular_velocity_covariance = [0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01]

                # 3. Linear Acceleration + Placeholder Covariance
                msg.linear_acceleration.x = data['ax']
                msg.linear_acceleration.y = data['ay']
                msg.linear_acceleration.z = data['az']
                msg.linear_acceleration_covariance = [0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1]

                self.imu_pub.publish(msg)
                
            except Exception:
                pass

def main(args=None):
    rclpy.init(args=args)
    node = ScunGunBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()