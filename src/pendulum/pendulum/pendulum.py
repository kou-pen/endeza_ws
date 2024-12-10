import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import pigpio
import time

kPGain = 0.1
kIGain = 0.1
kDGain = 0.1
TargetAngle = 0.0
class Pendulum(Node):
    node_name = 'pendulum'
    PWM1_PIN = [17, 18]
    PWM2_PIN = [19, 20]
    FREQ = 100
    RANGE = 255
    
    def __init__(self):
        super().__init__(self.node_name)
        self.pi = pigpio.pi()
        self.angle_sub = self.create_subscription(Float64, 'angle', self.angle_callback, 10)
        self.time_saver = time.time()
        self.prev_error = 0
        print('Pendulum node has been created')
        
        for pin in self.PWM1_PIN:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.set_PWM_frequency(pin, self.FREQ)
            self.pi.set_PWM_range(pin, self.RANGE)
            self.pi.set_PWM_dutycycle(pin, 0)
        
        for pin in self.PWM2_PIN:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.set_PWM_frequency(pin, self.FREQ)
            self.pi.set_PWM_range(pin, self.RANGE)
            self.pi.set_PWM_dutycycle(pin, 0)
        
    def angle_callback(self, angle):
        error = TargetAngle - angle.data
        error_sum += error * (time.time() - self.time_saver)
        error_diff = (error - self.prev_error) / (time.time() - self.time_saver)
        
        power = kPGain * error + kIGain * error_sum + kDGain * error_diff
        
        self.time_saver = time.time()
        self.prev_error = error
        
        if power > 0:
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], power)
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], 0)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], 0)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], -power)
        else:
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], 0)
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], -power)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], power)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], 0)
        
        print('angle: ', angle.data, 'power: ', power)
        print('error: ', error, 'error_sum: ', error_sum, 'error_diff: ', error_diff)

def main(args=None):
    rclpy.init(args=args)
    pendulum = Pendulum()
    rclpy.spin(pendulum)
    pendulum.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
            
    
