from std_srvs.srv import SetBool

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawNumberNode(Node):
    def __init__(self):
        super().__init__('draw_number')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.timer_period = 0.2
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.tiempo_transcurrido = 0.0
        self.estado = 'DIBUJANDO_EL_1'
        
        self.get_logger().info('Nodo iniciado. Preparado para dibujar el número 1...')

        self.pausado = False
        self.srv = self.create_service(SetBool, 'control_dibujo', self.control_dibujo_callback)
        self.get_logger().info('Servicio /control_dibujo listo.')

    def timer_callback(self):
        msg = Twist()
        if self.pausado:
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
                self.get_logger().info('¡Línea del 1 terminada, rotando 180 grados.')

        elif self.estado == 'ROTANDO_180':
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period

            if self.tiempo_transcurrido >= 6.28:
                self.estado = 'REGRESANDO_AL_CENTRO'
                self.tiempo_transcurrido = 0.0
                self.get_logger().info('¡Giro terminado, regresando al centro')
        
        elif self.estado == 'REGRESANDO_AL_CENTRO':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
        
            if self.tiempo_transcurrido >= 1.5:
                self.estado = 'ROTANDO_90'
                self.tiempo_transcurrido = 0.0
                self.get_logger().info('¡En el centro! Rotando 90 grados.')
        
        elif self.estado == 'ROTANDO_90':
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period

            if self.tiempo_transcurrido >= 3.14:
                self.estado = 'MOVIENDO_A_INICIO_DEL_0'
                self.tiempo_transcurrido = 0.0
                self.get_logger().info('¡Giro terminado, Deteniendo robot')
        
        elif self.estado == 'MOVIENDO_A_INICIO_DEL_0':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
        
            if self.tiempo_transcurrido >= 2:
                self.estado = 'MOVIENDO_A_INICIO_DEL_0_2'
                self.tiempo_transcurrido = 0.0
                self.get_logger().info('¡En el centro! Rotando 90 grados.')

        elif self.estado == 'MOVIENDO_A_INICIO_DEL_0_2':
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.tiempo_transcurrido += self.timer_period
        
            if self.tiempo_transcurrido >= 2.0:
                self.estado = 'ROTANDO_PARA_EL_0' 
                self.tiempo_transcurrido = 0.0
                self.get_logger().info('¡Margen alcanzado! Girando hacia abajo para iniciar el 0...')

        elif self.estado == 'ROTANDO_PARA_EL_0':
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            self.tiempo_transcurrido += self.timer_period

            if self.tiempo_transcurrido >= 3.14:
                self.estado = 'DIBUJANDO_EL_0'
                self.tiempo_transcurrido = 0.0
                self.get_logger().info('¡Orientación correcta! Trazando círculo antihorario...')
        
        elif self.estado == 'DIBUJANDO_EL_0':
            msg.linear.x = 0.15
            msg.angular.z = 0.5
            self.tiempo_transcurrido += self.timer_period

            if self.tiempo_transcurrido >= 12.56: 
                self.estado = 'FIN'
                self.tiempo_transcurrido = 0.0
                self.get_logger().info('¡Número 10 completado con éxito! Deteniendo robot.')
                
        elif self.estado == 'FIN':
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher_.publish(msg)

    def control_dibujo_callback(self, request, response):
        if request.data:
            self.pausado = True
            response.success = True
            response.message = "Dibujo DETENIDO temporalmente."
            self.get_logger().info('Servicio recibido: Deteniendo dibujo.')
        else:
            self.pausado = False
            response.success = True
            
            if self.estado == 'FIN':
                self.estado = 'DIBUJANDO_EL_1'
                self.tiempo_transcurrido = 0.0
                response.message = "Dibujo REINICIADO desde el principio."
                self.get_logger().info('Servicio recibido: Reiniciando dibujo.')
            else:
                response.message = "Dibujo REANUDADO."
                self.get_logger().info('Servicio recibido: Reanudando dibujo.')
                
        return response

def main(args=None):
    rclpy.init(args=args)
    node = DrawNumberNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()