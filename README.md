# Robot-livreur-de-medicament

Project Overview:--------------------
Welcome to our R&D project repository, where we present our autonomous robotic solution designed to enhance sample delivery efficiency in laboratory environments.

Problem Statement
In many laboratories, samples are created in various separate rooms and ultimately stored in a central inventory. When a researcher needs one or multiple samples, they typically have to leave their workspace and retrieve them manually. This process is time-consuming, disrupts focus, and reduces overall productivity.

Our Solution:----------------
To address this issue, we developed an autonomous mobile robot capable of delivering samples directly to researchers. The robot:

Navigates autonomously through laboratory corridors.

Locates and enters designated rooms.

Identifies samples using barcode scanning.

Picks up and drops off samples based on researcher requests.

Uses a charging station to manage its power autonomously.

This solution reduces the need for manual sample retrieval and allows researchers to stay focused on their work.

Hardware Platform-----------------------------------
We used TurtleBot 3, a compact, cost-effective, and programmable mobile robot developed by ROBOTIS in collaboration with the Open Source Robotics Foundation (OSRF). It’s well-suited for research and educational purposes.

Sensors Used:

LiDAR: For SLAM (Simultaneous Localization and Mapping) and obstacle detection.

Camera: Used for barcode scanning and enhanced object detection through sensor fusion.

Simulation Environment: Gazebo-----------------------------------
We used Gazebo, an open-source 3D robotics simulator, to test and validate our robot in a realistic virtual laboratory environment before deploying it in real life.

Why Gazebo?
Gazebo offers:

High-fidelity physics-based simulation (using ODE or Bullet engines).

Realistic 3D rendering of environments and objects.

Native support for various sensors (LiDAR, cameras, IMUs, etc.).

Seamless integration with ROS 1 and ROS 2.

A plugin system to extend functionality.

Multi-robot and collaborative scenario support.

Application in Our Project:---------------------------------
Simulating a full-scale laboratory environment with different sample rooms and corridors.

Testing robot navigation, SLAM, and object detection capabilities.

Verifying autonomous behavior and sample handling logic before real-world testing.
