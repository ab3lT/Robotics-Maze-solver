# Use ROS 2 Foxy base image with desktop support
FROM osrf/ros:foxy-desktop

# Set Arguments for user setup
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create non-root user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

# Update package lists
RUN sudo apt update && sudo apt upgrade -y

# Install essential tools
RUN sudo apt install -y \
    git curl wget sudo nano build-essential

# Install Gazebo 11 and ROS 2 Gazebo packages
RUN sudo apt install -y \
    gazebo11 \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-gazebo-ros2-control

# Install `joint_state_publisher_gui`
RUN sudo apt install -y ros-${ROS_DISTRO}-joint-state-publisher-gui

# Set up Gazebo environment variables
RUN echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:/usr/share/gazebo-11/models" >> ~/.bashrc && \
    echo "export GAZEBO_RESOURCE_PATH=\$GAZEBO_RESOURCE_PATH:/usr/share/gazebo-11" >> ~/.bashrc && \
    echo "export GAZEBO_PLUGIN_PATH=\$GAZEBO_PLUGIN_PATH:/usr/lib/x86_64-linux-gnu/gazebo-11/plugins" >> ~/.bashrc && \
    echo "export DISPLAY=\$DISPLAY" >> ~/.bashrc && \
    echo "export QT_X11_NO_MITSHM=1" >> ~/.bashrc

# Install GUI dependencies for Gazebo rendering
RUN sudo apt install -y \
    libxrandr2 libxinerama1 libxcursor1 libxi6 libxtst6 \
    libgl1-mesa-glx x11-apps mesa-utils x11-utils

# Allow Docker to access host display
RUN echo "xhost +local:docker" >> ~/.bashrc

# Install ROS dependencies
RUN rosdep update

# Source ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

# Expose Gazebo ports
EXPOSE 11345

# Default command: Launch Gazebo with ROS 2 support
CMD ["gazebo", "--verbose"]
