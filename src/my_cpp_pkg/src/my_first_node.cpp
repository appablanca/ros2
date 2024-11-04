#include "rclcpp/rclcpp.hpp"

class my_first_node : public rclcpp::Node
{
public:
    my_first_node() : Node("cpp_test")
    {
        RCLCPP_INFO(this->get_logger(), "MERHABA AMK");
        timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&my_first_node::timer, this));
    }

private:
    void timer()
    {
        RCLCPP_INFO(this->get_logger(), "sa");
    }
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<my_first_node>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 1;
}