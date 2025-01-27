Answer Number 1 :
1. Run the Docker Container in Interactive Mode
To run the Docker container with the python:3.12.8 image and use bash as the entrypoint, use the following command:
```bash
docker run -it --entrypoint bash python:3.12.8
```
2. Check the Version of pip
Once inside the container, use the following command to check the version of pip installed:
```bash
pip --version
```
3. Result
After running the command, you should see an output similar to the following:
```bash
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

Answer Number 2 :
db:5432

Answer

