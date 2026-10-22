import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_srvs.srv import SetBool

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('g10_obstacle_avoidance')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        self.timer_period = 0.2
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.tiempo_transcurrido = 0.0
        self.estado = 'DIBUJANDO_EL_1'
        self.pausado = False
        
        # Variables de desviación dinámica
        self.esquivando = False
        self.giro_esquiva = 0.0

        self.srv = self.create_service(SetBool, 'control_dibujo', self.control_dibujo_callback)
        self.get_logger().info('Nodo Obstacle Avoidance (Grupo 10) Iniciado.')

    def scan_callback(self, msg):
        # Analizamos sectores izquierdo (0 a 45) y derecho (315 a 359) para decidir hacia dónde esquivar
        frente_izq = msg.ranges[0:45]
        frente_der = msg.ranges[315:360]
        
        valid_izq = [r for r in frente_izq if r > msg.range_min and r < msg.range_max]
        valid_der = [r for r in frente_der if r > msg.range_min and r < msg.range_max]
        
        min_izq = min(valid_izq) if valid_izq else 3.5
        min_der = min(valid_der) if valid_der else 3.5
        
        # Si el camino está comprometido a menos de 0.6 metros
        if min_izq < 0.6 or min_der < 0.6:
            self.esquivando = True
            # Si hay más espacio a la izquierda, gira de manera horaria y viceversa (sin detener el avance lineal)
            if min_izq > min_der:
                self.giro_esquiva = 0.4  # Gira a la izquierda
            else:
                self.giro_esquiva = -0.4 # Gira a la derecha
        else:
            self.esquivando = False

    def timer_callback(self):
        msg = Twist()
        if self.pausado:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            return 

        # Modificación dinámica si hay que esquivar sobre la marcha
        if self.esquivando and self.estado != 'FIN':
            msg.linear.x = 0.12     # Reduce un poco la velocidad, pero NUNCA se detiene
            msg.angular.z = self.giro_esquiva
            self.publisher_.publish(msg)
            return

        # --- LÓGICA DE DIBUJO DEL NÚMERO 10 ---
        if self.estado == 'DIBUJANDO_EL_1':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 3.0: self.estado = 'ROTANDO_180'; self.tiempo_transcurrido = 0.0
        elif self.estado == 'ROTANDO_180':
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 6.28: self.estado = 'REGRESANDO_AL_CENTRO'; self.tiempo_transcurrido = 0.0
        elif self.estado == 'REGRESANDO_AL_CENTRO':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 1.5: self.estado = 'ROTANDO_90'; self.tiempo_transcurrido = 0.0
        elif self.estado == 'ROTANDO_90':
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 3.14: self.estado = 'MOVIENDO_A_INICIO_DEL_0'; self.tiempo_transcurrido = 0.0
        elif self.estado == 'MOVIENDO_A_INICIO_DEL_0':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 2: self.estado = 'MOVIENDO_A_INICIO_DEL_0_2'; self.tiempo_transcurrido = 0.0
        elif self.estado == 'MOVIENDO_A_INICIO_DEL_0_2':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 2.0: self.estado = 'ROTANDO_PARA_EL_0'; self.tiempo_transcurrido = 0.0
        elif self.estado == 'ROTANDO_PARA_EL_0':
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 3.14: self.estado = 'DIBUJANDO_EL_0'; self.tiempo_transcurrido = 0.0
        elif self.estado == 'DIBUJANDO_EL_0':
            msg.linear.x = 0.15
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period
            if self.tiempo_transcurrido >= 12.56: self.estado = 'FIN'; self.tiempo_transcurrido = 0.0
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
    node = ObstacleAvoidanceNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()