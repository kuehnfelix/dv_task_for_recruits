#pragma once

#include <vector>

enum class Color {
    BLUE,
    YELLOW,
    ORANGE
};

struct Cone {
    Color color;
    double x;
    double y;

    Cone(Color c, double x_val, double y_val) : color(c), x(x_val), y(y_val) {}
};

struct Point2D {
    double x;
    double y;

    Point2D(double x_val, double y_val) : x(x_val), y(y_val) {}
};

struct CarState {
    double x;
    double y;
    double theta; // orientation angle in radians

    CarState(double x_val, double y_val, double theta_val) : x(x_val), y(y_val), theta(theta_val) {}
};

std::vector<Point2D> calcCenterline(const std::vector<Cone>& cones, const CarState& car_state);