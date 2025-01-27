Answer Number 1 :
1. Run the Docker Container in Interactive Mode
To run the Docker container with the python:3.12.8 image and use bash as the entrypoint, use the following command:
docker run -it --entrypoint bash python:3.12.8
2. Check the Version of pip
Once inside the container, use the following command to check the version of pip installed:
pip --version

