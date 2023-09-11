# Density-Based-Traffic-Signal-Control-Using-Image-Processing

### Project Description:
This GitHub repository hosts the source code and documentation for a groundbreaking project that controls traffic signals based on image processing techniques. Instead of relying on traditional timers or electronic sensors, The system detects vehicles using cameras and adjusts traffic lights accordingly. Here's a detailed overview of this project:

## Disclaimer: Improved Performance with OpenCV CUDA

For enhanced performance and real-time processing, we recommend using OpenCV with CUDA support. OpenCV CUDA harnesses the power of NVIDIA GPUs to accelerate image processing tasks.

To take full advantage of GPU acceleration, make sure you have OpenCV built with CUDA support and have compatible NVIDIA drivers installed on your system. You can check OpenCV's official documentation for instructions on building OpenCV with CUDA: [OpenCV CUDA Installation Guide](https://docs.opencv.org/master/d5/de5/tutorial_py_setup_in_windows.html).

By using OpenCV with CUDA, you can expect significant speed improvements in tasks such as image detection and processing, making this project even more efficient.


## Project Overview:
### Vehicle Detection and Traffic Signal Control
We employ image-processing algorithms to detect vehicles. A single camera mounted on a motor captures continuous video footage of lanes, covering angles from 0 to 180 degrees. Each video frame is analyzed, and the system calculates the total number of vehicles present.

### Prioritizing Traffic Signals
This system prioritizes traffic signals based on vehicle density. Lanes with the highest vehicle count are given a green light first, followed by other lanes. This dynamic approach ensures efficient traffic flow and minimizes congestion.

## Key Objectives:
- **Dynamic Prioritization**: Prioritize lanes based on real-time vehicle density.
- **System Robustness**: Implement a default traffic signal pattern in case of system failure.
- **Time Efficiency**: Ensure every lane receives a green light within a predefined time frame.

## Advantages of this Approach:
- **Comprehensive Traffic Data**: This video-based system offers detailed traffic information.
- **Integrated Technology**: It combines surveillance and traffic control, optimizing traffic management.
- **Time Optimisation**: Effective time utilisation, reducing man-hours wasted at traffic signals.
- **Safety Enhancement**: Eliminates the need for traffic personnel at junctions and reduces accidents.
Implementation:

The project is implemented in Python, leveraging the power of image processing and video analysis. The rotating camera provides a 180-degree view, allowing comprehensive coverage of traffic lanes. The system dynamically adjusts traffic signals, making it an invaluable tool for traffic analysis and performance enhancement.


### Acknowledgments

This project builds upon the work of Pysource(https://www.youtube.com/@pysource-com) for the initial code inspiration and guidance. I am grateful for his valuable contributions to the community.
