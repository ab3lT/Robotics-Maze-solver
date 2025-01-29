FROM osrf/ros:foxy-desktop

# Add ubuntu user with same UID and GID as your host system
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if ! id -u $USER_UID >/dev/null 2>&1; then \
    groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi
# Add sudo support for the non-root user
RUN apt-get update && \
    apt-get install -y sudo && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to the non-root user
USER $USERNAME

# Add user to video group for webcam access
RUN sudo usermod --append --groups video $USERNAME

# Update all packages
RUN sudo apt update && sudo apt upgrade -y

# Install Git
RUN sudo apt install -y git

# Install Gazebo Classic (Gazebo 11)
RUN sudo apt install -y gazebo11 ros-${ROS_DISTRO}-gazebo-ros-pkgs ros-${ROS_DISTRO}-gazebo-ros2-control

# Set environment variables for Gazebo
RUN echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:/usr/share/gazebo-11/models" >> ~/.bashrc && \
    echo "export GAZEBO_RESOURCE_PATH=\$GAZEBO_RESOURCE_PATH:/usr/share/gazebo-11" >> ~/.bashrc && \
    echo "export GAZEBO_PLUGIN_PATH=\$GAZEBO_PLUGIN_PATH:/usr/lib/x86_64-linux-gnu/gazebo-11/plugins" >> ~/.bashrc && \
    echo "export DISPLAY=:0" >> ~/.bashrc

# Install dependencies for GUI support (optional)
RUN sudo apt install -y mesa-utils x11-apps x11-utils

# Rosdep update
RUN rosdep update

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

# Expose Gazebo ports
EXPOSE 11345

# Start Gazebo automatically when the container runs (optional)
CMD ["gazebo"]
