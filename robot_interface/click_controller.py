import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import cv2
import numpy as np


class ClickController(Node):

    def __init__(self):
        super().__init__('click_controller')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        self.width = 640
        self.height = 480

        self.image = 255 * np.ones((self.height, self.width, 3), dtype=np.uint8)

        cv2.namedWindow("Control Window")
        cv2.setMouseCallback("Control Window", self.mouse_callback)

        self.timer = self.create_timer(0.1, self.update_window)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            msg = Twist()

            if y < self.height / 2:
                msg.linear.x = 0.2
                self.get_logger().info("Moving forward")
            else:
                msg.linear.x = -0.2
                self.get_logger().info("Moving backward")

            self.publisher_.publish(msg)

    def update_window(self):
        display = self.image.copy()
        cv2.line(
            display,
            (0, int(self.height / 2)),
            (self.width, int(self.height / 2)),
            (0, 0, 255),
            2
        )
        cv2.imshow("Control Window", display)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = ClickController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
