import math
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        time.sleep(1)

        self.dibujar_10()

    def parar(self):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        self.publisher.publish(msg)

        time.sleep(0.2)

    def mover_recto(self, velocidad, tiempo):

        msg = Twist()

        msg.linear.x = velocidad
        msg.angular.z = 0.0

        inicio = time.time()

        while time.time() - inicio < tiempo:

            self.publisher.publish(msg)

            time.sleep(0.02)

        self.parar()

    def girar(self, velocidad_angular, angulo):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = velocidad_angular

        tiempo = abs(angulo / velocidad_angular)

        inicio = time.time()

        while time.time() - inicio < tiempo:

            self.publisher.publish(msg)

            time.sleep(0.02)

        self.parar()


    def dibujar_circulo(self):

        msg = Twist()

        msg.linear.x = 0.6
        msg.angular.z = 0.6

        tiempo = (2.0 * math.pi) / 0.6

        inicio = time.time()

        while time.time() - inicio < tiempo:

            self.publisher.publish(msg)

            time.sleep(0.02)

        self.parar()

    def dibujar_10(self):

        self.get_logger().info(
            'Comenzando a dibujar el 10'
        )

        self.girar(
            velocidad_angular=1.0,
            angulo=math.pi / 2
        )

        self.mover_recto(
            velocidad=1.0,
            tiempo=4.0
        )


        self.girar(
            velocidad_angular=1.0,
            angulo=math.pi
        )

        self.mover_recto(
            velocidad=1.0,
            tiempo=2.0
        )


        self.girar(
            velocidad_angular=1.0,
            angulo=math.pi / 2
        )

        self.mover_recto(
            velocidad=1.0,
            tiempo=1.5
        )

        self.dibujar_circulo()

        self.parar()

        self.get_logger().info(
            '10 terminado'
        )


def main(args=None):

    rclpy.init(args=args)

    nodo = TurtleController()

    try:

        rclpy.spin(nodo)

    except KeyboardInterrupt:

        pass

    finally:

        nodo.parar()

        nodo.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':
    main()
