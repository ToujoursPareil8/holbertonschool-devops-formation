# 1-first_image

This project contains a tiny Python (Flask) web application, containerized using Docker.

## Build the image
To build the Docker image, navigate to this directory and run the following command. The `-t` flag tags the image with a readable name (`first-python-app`).

```bash
docker build -t first-python-app .
docker run -d -p 5000:5000 --name my-running-python-app first-python-app
```