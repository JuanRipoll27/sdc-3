# set the base image. Since we're running
# a Python application a Python base image is used FROM python:3.8
# set a key-value label for the Docker image
FROM python:3.8

# The LABEL instruction is optional and 
# adds metadata to an image.
# A LABEL is a key-value pair that can be used to help
# identify the image, typically with information like the
# version, description, and maintainer.
# Here we're setting the maintainer label to "moh"
LABEL maintainer="moh"

# copy files from the host to the container filesystem. 
# For example, all the files in the current directory
# to the  `/app` directory in the container
COPY . /app


# Defines the working directory within the container
# With WORKDIR, you can set the working directory 
# for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions
# that follow it in the Dockerfile.
WORKDIR /app

# run commands within the container. 
# For example, invoke a pip command 
# to install dependencies defined in the requirements.txt file. 
RUN pip install -r requirements.txt

# provide a command to run on container start. 
# For example, start the `app.py` application.
CMD [ "python", "app.py" ]
