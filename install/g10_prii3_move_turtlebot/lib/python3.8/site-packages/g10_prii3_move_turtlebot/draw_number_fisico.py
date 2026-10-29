import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool


class DrawNumberNode(Node):
    """Ejemplo temporizado de movimiento para trazar aproximadamente el 10."""

    def __init__(self):
        super().__init__('draw_number')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.elapsed = 0.0
        self.state = 0
        self.paused = False
        self.steps = [
            (0.12, 0.0, 3.0, 'tramo recto'),
            (0.0, 0.35, 8.98, 'giro de 180 grados'),
            (0.12, 0.0, 1.5, 'regreso'),
            (0.0, 0.35, 4.49, 'giro de 90 grados'),
            (0.12, 0.0, 2.0, 'desplazamiento'),
            (0.12, 0.0, 2.0, 'desplazamiento'),
            (0.0, -0.35, 4.49, 'orientación para el cero'),
            (0.10, 0.35, 12.56, 'trazado aproximado del cero'),
        ]
        self.srv = self.create_service(SetBool, '/control_dibujo', self.control_callback)
        self.get_logger().info('Nodo de trazado iniciado. Prueba primero en Gazebo.')

    def timer_callback(self):
        msg = Twist()
        if self.paused or self.state >= len(self.steps):
            self.publisher_.publish(msg)
            return
        linear, angular, duration, description = self.steps[self.state]
        msg.linear.x = linear
        msg.angular.z = angular
        self.elapsed += self.timer_period
        if self.elapsed >= duration:
            self.get_logger().info(f'Finalizado: {description}')
            self.state += 1
            self.elapsed = 0.0
        self.publisher_.publish(msg)

    def control_callback(self, request, response):
        if request.data:
            self.paused = True
            response.message = 'Movimiento pausado.'
        else:
            if self.state >= len(self.steps):
                self.state = 0
                self.elapsed = 0.0
            self.paused = False
            response.message = 'Movimiento reanudado; si ya terminó, reiniciado.'
        response.success = True
        return response


def main(args=None):
    rclpy.init(args=args)
    node = DrawNumberNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publisher_.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
