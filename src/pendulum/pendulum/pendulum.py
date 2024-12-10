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
        self.error = 0
        self.error_sum = 0
        self.error_diff = 0
        
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
        self.error = TargetAngle - angle.data
        self.error_sum += self.error * (time.time() - self.time_saver)
        self.error_diff = (self.error - self.prev_error) / (time.time() - self.time_saver)
        
        power = kPGain * self.error + kIGain * self.error_sum + kDGain * self.error_diff
        
        self.time_saver = time.time()
        self.prev_error = self.error
        
        if power > 0:
            duty_cycle = max(0, min(power * 100, 255))  # Clamp to the range [0, 255]
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], duty_cycle)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], duty_cycle)
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], 0)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], 0)
        else:
            duty_cycle = max(0, min(power * 100, 255))
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], 0)
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], duty_cycle)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], duty_cycle)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], 0)
        
        print('angle: ', angle.data, 'power: ', power)
        print('error: ', self.error, 'error_sum: ', self.error_sum, 'error_diff: ', self.error_diff)

def main(args=None):
    rclpy.init(args=args)
    pendulum = Pendulum()
    rclpy.spin(pendulum)
    pendulum.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
            
    
