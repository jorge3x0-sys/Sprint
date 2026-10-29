import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_srvs.srv import SetBool

class CollisionAvoidanceNode(Node):
    def __init__(self):
        super().__init__('g10_collision_avoidance')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Suscripción al LiDAR del TurtleBot
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        
        self.timer_period = 0.2
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.tiempo_transcurrido = 0.0
        self.estado = 'DIBUJANDO_EL_1'
        self.pausado = False
        self.obstaculo_detectado = False
        
        # Servicio heredado de control manual
        self.srv = self.create_service(SetBool, 'control_dibujo', self.control_dibujo_callback)
        self.get_logger().info('Nodo Collision Avoidance (Grupo 10) Iniciado.')

    def scan_callback(self, msg):
        rangos_frente = msg.ranges[0:15] + msg.ranges[345:360]
        
        lecturas_validas = [r for r in rangos_frente if r > msg.range_min and r < msg.range_max]
        
        if lecturas_validas:
            distancia_minima = min(lecturas_validas)

            if distancia_minima < 0.5:
                if not self.obstaculo_detectado:
                    self.get_logger().warn(f'¡Obstáculo al frente detectado a {distancia_minima:.2f}m! Deteniendo marcha...')
                self.obstaculo_detectado = True
            else:
                if self.obstaculo_detectado:
                    self.get_logger().info('Obstáculo despejado. Reanudando marcha.')
                self.obstaculo_detectado = False

    def timer_callback(self):
        msg = Twist()

        if self.pausado or self.obstaculo_detectado:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            return 

        if self.estado == 'DIBUJANDO_EL_1':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 3.0:
                self.estado = 'ROTANDO_180'
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'ROTANDO_180':
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 6.28:
                self.estado = 'REGRESANDO_AL_CENTRO'
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'REGRESANDO_AL_CENTRO':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 1.5:
                self.estado = 'ROTANDO_90'
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'ROTANDO_90':
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 3.14:
                self.estado = 'MOVIENDO_A_INICIO_DEL_0'
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'MOVIENDO_A_INICIO_DEL_0':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 2:
                self.estado = 'MOVIENDO_A_INICIO_DEL_0_2'
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'MOVIENDO_A_INICIO_DEL_0_2':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 2.0:
                self.estado = 'ROTANDO_PARA_EL_0' 
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'ROTANDO_PARA_EL_0':
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 3.14:
                self.estado = 'DIBUJANDO_EL_0'
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'DIBUJANDO_EL_0':
            msg.linear.x = 0.15
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 12.56: 
                self.estado = 'FIN'
                self.tiempo_transcurrido = 0.0
        elif self.estado == 'FIN':
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher_.publish(msg)

    def control_dibujo_callback(self, request, response):
        if request.data:
            self.pausado = True
            response.success = True
            response.message = "Dibujo DETENIDO por servicio."
        else:
            self.pausado = False
            response.success = True
            if self.estado == 'FIN':
                self.estado = 'DIBUJANDO_EL_1'
                self.tiempo_transcurrido = 0.0
                response.message = "Dibujo REINICIADO."
            else:
                response.message = "Dibujo REANUDADO."
        return response

def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()