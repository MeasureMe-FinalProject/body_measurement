# Body Measurement and Size Recommendation System

This project provides tools to build a body measurement and size recommendation system. You can run this system locally on your machine or using Docker.

## Prerequisites

- **Python**: The system requires Python 3. Make sure Python is installed on your machine. If not, download and install it from the [official Python website](https://www.python.org/downloads/).
- **Docker**: For running the system in a Docker container, ensure Docker is installed. If not, install it from the [Official Docker Website](https://docker.com).

## Initial Setup

To get started, clone the repository to obtain the latest version of the system:

```bash
git clone https://github.com/MeasureMe-FinalProject/body_measurement
```

## Running Locally

### Setup

1. Open a terminal or command prompt.
2. Navigate to the project's root directory.
3. Optionally, create a Python virtual environment to isolate package dependencies.
4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Launch

Run the system by executing:

```bash
python debug.py
```

This will start the system locally, allowing direct interaction on your machine.

## Using Docker (Recommended)

### Docker Setup

1. Navigate to the project directory in a terminal.
2. Build the Docker image (replace `<image-name>` with a name of your choice for the Docker image):
   ```bash
   docker build -t <image-name> .
   ```

### Running the Docker Container

1. Run the Docker container by mapping the ports:
```bash
    docker run -p <host-port>:<container-port> <image-name>
```

   Replace `<host-port>` and `<container-port>` with the port numbers you want to use for the host machine and the container, respectively. Ensure that `<image-name>` matches the name you used when building the Docker image.

## Conclusion

By following these instructions, you can run the system either locally or using Docker, depending on your preference and development environment setup. This flexibility allows you to develop and test in an environment that matches your deployment strategy.

