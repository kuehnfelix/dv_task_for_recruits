#include "matplotlibcpp.h"
#include <cmath>
#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <vector>

#include "task.h"

namespace plt = matplotlibcpp;

class Sim {
public:
  Sim() : car_state(0, 0, 0) { 
    plt::ion(); 
    // use tkagg
    plt::backend("TkAgg");
    car_state = CarState(0, 0, 0);
  }

  void loadTrackFromCSV(const std::string &file_path) {
    std::ifstream file(file_path);
    std::string line;
    cones.clear();

    if (!file.is_open()) {
      std::cerr << "Failed to open file: " << file_path << std::endl;
      return;
    }

    while (std::getline(file, line)) {
      std::istringstream stream(line);
      std::string color, x_str, y_str;

      // Read color, x, and y as comma-separated values
      if (!std::getline(stream, color, ',') ||
          !std::getline(stream, x_str, ',') ||
          !std::getline(stream, y_str, ',')) {
        std::cerr << "Error parsing line: " << line << std::endl;
        continue; // Skip this line if parsing fails
      }

      // Convert x and y from strings to doubles
      double x, y;
      try {
        x = std::stod(x_str);
        y = std::stod(y_str);
      } catch (const std::invalid_argument &) {
        std::cerr << "Invalid coordinates in line: " << line << std::endl;
        continue;
      }

      // Determine the color and add to cones
      if (color == "BLUE") {
        cones.emplace_back(Color::BLUE, x, y);
      } else if (color == "YELLOW") {
        cones.emplace_back(Color::YELLOW, x, y);
      } else if (color == "ORANGE") {
        cones.emplace_back(Color::ORANGE, x, y);
      } else {
        std::cerr << "Unknown color: " << color << " in line: " << line
                  << std::endl;
      }
    }

    file.close();
    std::cout << "Loaded " << cones.size() << " cones from CSV."
              << std::endl; // Final confirmation
  }

  void simulationStep() {
    if (centerline.size() >= 1) {
      // Update car's position based on the centerline points
      float direction_x = centerline[0].x - car_state.x;
      float direction_y = centerline[0].y - car_state.y;
      float distance =
          std::sqrt(direction_x * direction_x + direction_y * direction_y);

      car_state.x += 0.1 * direction_x / distance;
      car_state.y += 0.1 * direction_y / distance;
      car_state.theta = std::atan2(direction_y, direction_x);
    }

    visible_cones = getVisibleCones();
    std::vector<Cone> transformed_cones = transformConesToCarFrame();

    // Compute the centerline (this function needs to be implemented)
    centerline = calcCenterline(transformed_cones, car_state);
  }

  void visualize() {
    // Clear the previous plot
    plt::clf();

    // Plot visible cones
    for (const auto &cone : visible_cones) {
      std::string color;
      if (cone.color == Color::BLUE)
        color = "blue";
      else if (cone.color == Color::YELLOW)
        color = "yellow";
      else
        color = "orange";

      plt::plot({cone.x}, {cone.y}, {{"marker", "o"}, {"color", color}});
    }

    // Plot the car's position as an arrow
    double car_length = 1.0;
    double dx = car_length * std::cos(car_state.theta);
    double dy = car_length * std::sin(car_state.theta);
    // plt::arrow(car_state.x, car_state.y, dx, dy, 0.5, {{"color", "blue"}});

    // Plot the centerline
    if (!centerline.empty()) {
      std::vector<double> cx, cy;
      for (const auto &point : centerline) {
        cx.push_back(point.x);
        cy.push_back(point.y);
      }
      plt::plot(cx, cy, "r-");
    }
    std::cout << "Car position: (" << car_state.x << ", " << car_state.y
              << "), theta: " << car_state.theta << std::endl;

    unsigned box_length = 25;

    float d_x = (box_length/2) * std::cos(car_state.theta);
    float d_y = (box_length/2) * std::sin(car_state.theta);

    float center_x = car_state.x + d_x;
    float center_y = car_state.y + d_y;    

    plt::xlim(center_x - 15, center_x + 15);
    plt::ylim(center_y - 15, center_y + 15);

    // Draw and pause to create animation effect
    plt::pause(0.1);
  }

private:
  std::vector<Cone> cones;
  std::vector<Cone> visible_cones;
  std::vector<Point2D> centerline;
  CarState car_state;

  double piToPi(double angle) { return std::remainder(angle, 2 * M_PI); }

  std::vector<Cone> transformConesToCarFrame() {
    std::vector<Cone> transformed;
    for (const auto &cone : visible_cones) {
      // Translate cone position relative to the car
      double dx = cone.x - car_state.x;
      double dy = cone.y - car_state.y;

      // Rotate based on car's orientation (theta)
      double rotated_x =
          dx * std::cos(-car_state.theta) - dy * std::sin(-car_state.theta);
      double rotated_y =
          dx * std::sin(-car_state.theta) + dy * std::cos(-car_state.theta);

      transformed.emplace_back(cone.color, rotated_x, rotated_y);
    }
    return transformed;
  }

  std::vector<Cone> getVisibleCones() {
    std::vector<Cone> visible_cones;
    for (const auto &cone : cones) {
      double dist_squared =
          std::pow(cone.x - car_state.x, 2) + std::pow(cone.y - car_state.y, 2);
      if (dist_squared < 625) { // Within visible range
        double detection_angle = piToPi(
            piToPi(std::atan2(cone.y - car_state.y, cone.x - car_state.x)) -
            piToPi(car_state.theta));
        if (std::fabs(detection_angle) < M_PI / 3) { // Within 60 degrees
          visible_cones.push_back(cone);
        }
      }
    }
    return visible_cones;
  }
};

int main() {
  Sim sim;
  sim.loadTrackFromCSV("track.csv");

  // Main loop for the simulation
  while (true) {
    sim.simulationStep();
    sim.visualize();
  }

  return 0;
}
