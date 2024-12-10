#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "geometry_msgs/msg/quaternion.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_broadcaster.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "std_msgs/msg/float64.hpp"

void geometry_quat_to_rpy(double &roll, double &pitch, double &yaw, const geometry_msgs::msg::Quaternion &geometry_quat)
{
  tf2::Quaternion q(geometry_quat.x, geometry_quat.y, geometry_quat.z, geometry_quat.w);
  tf2::Matrix3x3 m(q);
  m.getRPY(roll, pitch, yaw);
}

class Q2QPY : public rclcpp::Node {
public:
  Q2QPY() : Node("q2qpy") {
    sub_ = this->create_subscription<sensor_msgs::msg::Imu>("/imu/data", 10, std::bind(&Q2QPY::callback, this, std::placeholders::_1));
    pub_ = this->create_publisher<std_msgs::msg::Float64>("angle", 10);
  }
  
private:
  void callback(const sensor_msgs::msg::Imu::SharedPtr msg) {
    double roll, pitch, yaw;
    geometry_quat_to_rpy(roll, pitch, yaw, msg->orientation);
    std_msgs::msg::Float64 angle;
    angle.data = pitch;
    pub_->publish(angle);
    std::cout << "rpy:" << roll << " " << pitch << " " << yaw << std::endl;

  }
  
  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr sub_;
  rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pub_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Q2QPY>());
  rclcpp::shutdown();
  return 0;
}
