import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import pigpio
import time
import math

kPGain = 7700.0
kIGain = 600.0
kDGain = 45.0

TargetAngle = -0.190

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
        self.rotate_sub = self.create_subscription(Float64, 'rotate_power', self.rotate_callback, 10)
        self.time_saver = time.time()
        self.prev_error = 0
        self.error = 0
        self.error_sum = 0
        self.error_diff = 0
        self.diff_lr = 0
        self.power = 0
        
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
        
        self.power = kPGain * self.error + kIGain * self.error_sum + kDGain * self.error_diff
        
        self.time_saver = time.time()
        self.prev_error = self.error
        
        if (abs(angle.data) > (math.pi * 0.25)):
            self.error_sum = 0.0
            self.power = 0
        
        # if self.power > 0:
        #     duty_cycle_l = max(0, min(self.power + self.diff_lr, 255))  # Clamp to the range [0, 255]
        #     duty_cycle_r = max(0, min(self.power - self.diff_lr, 255)) # Clamp to the range [0, 255]
            
        #     self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], duty_cycle_l)
        #     self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], duty_cycle_r)
        #     self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], 0)
        #     self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], 0)
        # else:
        #     duty_cycle_l = max(0, min(self.diff_lr + self.power * -1, 255))
        #     duty_cycle_r = max(0, min(-self.diff_lr + self.power * -1, 255))
            
        #     self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], 0)
        #     self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], duty_cycle_r)
        #     self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], duty_cycle_l)
        #     self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], 0)
        
        duty_cycle_l = max(-255, min(self.diff_lr + self.power, 255))
        duty_cycle_r = max(-255, min(self.diff_lr - self.power, 255))
        
        if duty_cycle_l > 0:
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], 0)
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], duty_cycle_l)
        else:
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[0], duty_cycle_l * -1)
            self.pi.set_PWM_dutycycle(self.PWM1_PIN[1], 0)
            
        if duty_cycle_r > 0:
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], 0)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], duty_cycle_r)
        else:
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[0], duty_cycle_r * -1)
            self.pi.set_PWM_dutycycle(self.PWM2_PIN[1], 0)
        
        print('angle: ', angle.data, 'power: ', self.power)
        print('error: ', self.error, 'error_sum: ', self.error_sum, 'error_diff: ', self.error_diff)
        print('diff_lr: ', self.diff_lr)
        
    def rotate_callback(self, rotate_power):
        self.diff_lr = rotate_power.data

def main(args=None):
    rclpy.init(args=args)
    pendulum = Pendulum()
    try:
        rclpy.spin(pendulum)
    except KeyboardInterrupt:
        pendulum.pi.set_PWM_dutycycle(pendulum.PWM1_PIN[0], 0)
        pendulum.pi.set_PWM_dutycycle(pendulum.PWM1_PIN[1], 0)
        pendulum.pi.set_PWM_dutycycle(pendulum.PWM2_PIN[0], 0)
        pendulum.pi.set_PWM_dutycycle(pendulum.PWM2_PIN[1], 0)
        pendulum.destroy_node()
        rclpy.shutdown()
    
if __name__ == '__main__':
    main()
            
    
