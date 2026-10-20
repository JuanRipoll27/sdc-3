# type: ignore

# make your terminal concise
# Pro tip make your terminal prompt more concise
#%%bash
#export PS1="\W $ "


# echo test
# try running below line in vs code cell execute
# if it is being run using a python kernel, switch to the bash kernel
#%%bash
echo "hello test"

# If you're still having issues, it means that vs code is unable to recognize the bash kernel
# Please run all following commands inside a bash terminal


# First simply run the fast api app using uvicorn, and verify it is working
# %%bash
python app.py

# After verifying the app is working, have a look at the existing
# Dockerfile in the directory: 1-docker-hello-world/Dockerfile
# Inspect it and understand the commands in it
# it does contain the instructions to build the docker image
# for the fast api app

# Now build the docker image using the Dockerfile
# and the command below
# As you can see the docker build command takes the path to directory
# containing the Dockerfile as an argument
# %%bash
docker build . 

# After building the docker image, you should see the image 
# listed in the docker images list
# In this list you should be able to see the image you just built
# and also its size and image id
# %%bash
docker images

# You can also list all images using
# docker image ls
# %%bash
docker image ls

# Now, that you've listed the docker image that been created.
# You should notice that the repository and tag values are `<none>`
# The image is not tagged, and has a random id - We will get to this later

# So, all we have done is build the image, but we have not run the image
# Imagine it being an executable (*.exe) file, you have the file, 
# but you have not run it
# Run the docker image using the image id
# Now in can run the image using the the image id
# replace <image_id> with the id of the image
# %%bash
docker run <image_id>


# Based on the console output, you can see that app (=container) is running
# but if you try to access the app using the browser (using localhost:8080)
# you'll see that the app is not accessible
# This is because the app is running in the container, but the port
# is not exposed to the **host** machine
# It is very difficult to expose the port of a running container
# to the host machine, so we need to stop the container 
# and run a new container again with the port exposed
# So let's kill the running container, by interrupting the command 
# (using control c)

# After stopping the container, you should try to run the container again
# but this time with the port exposed, this can be achieved
# by running the -p flag with the docker run command
# If you're running the app in codespace
# you'll see a popup informing you that an app is running on the exposed 
# port, and you can click on the link to access the app
# %%bash
docker run -p 8080:8080 759217e5ba2c

# And voila! you should be able to access the app using the browser
# by going to localhost:8080 (or the exposed codespace url)

# So what did -p 8080:8080 do?
# It told docker to map the port 8080 of the host machine to the port 8080
# of the container
# The syntax is -p <host_port>:<container_port>
# So this means, you can map any port of the host machine to any port of the container
# For instance, we can make the app accessible on port 80 of the host machine
# by running the command below
# Make sure to stop the running container before running the command
# %%bash
docker run -p 80:8080 <image_id>

# Great you should be able to access the app using the browser
# What we have done so far is build the image, run the image a
# and expose it to a desired port

## A few things to note:
# 1. The image id is randomly generated, and it is difficult to remember
#    the image id, so it is recommended to tag the image
# 2. The image is not tagged, so let's tag the image
#    using the docker tag command
#    The syntax is docker tag <image_id> <tag_name>
#    Replace <image_id> with the image id and <tag_name> with the desired tag
# %%bash
docker tag <image_id> fhtw-hello-world


# After tagging the image, list all docker images again
# You should now see that values repository and tag of
# the image are not <none> anymore
# %%bash
docker images


# You should see that the repository and tag values are now fhtw-hello-world
# This is because we tagged the image with the tag fhtw-hello-world
# The image id is still the same, but the image has a tag now
# Now to make our life more convenient
# the image can be run using the tag as well
# %%bash
docker run -p 80:8080 fhtw-hello-world

# The container is running, and you can access the app using the browser
# but it is running in the foreground, and you cannot run any other command
# in the terminal
# You can run the container in the background using the -d flag
# -d stands for detached mode
# Interrupt the prevoius command (or in terminal using control c) and run the command below
# After running the command, you should see the container id returned to you
# %%bash
docker run -d -p 80:8080 fhtw-hello-world

# Now our application / the container is running in the background
# and you can run other commands in the terminal
# You can also see the running container using the command below
# %%bash
docker ps

# You can also see all containers (including the stopped ones) using
# the command below
# %%bash
docker ps -a


# A container can be stopped using the container id
# You can stop a running container using the command below
# Replace <container_id> with the container id
# %%bash
docker stop <container_id>


# After stopping the container
# you can see that the container is not running anymore
# by listing all running containers
# %%bash
docker ps

# A stopped container can be started again (resume) using the container id
# You can start a stopped container using the command below
# Replace <container_id> with the container id
# %%bash
docker start <container_id>

# Verify that the container is running again
# by listing all running containers
# %%bash
docker ps

# You may have noticed that a container has a name
# The name is randomly generated but like the image tag
# it can be used to address a container
# Run docker ps again, and have a look at the name of the container
# You can also start/stop a running container using the name
# %%bash
docker stop <container_name>


# You can also restart (stop and start) a running container using the container id
# You can restart a running container using the command below
# Replace <container_id> with the container id
# %%bash
docker restart <container_id> OR <container_name>

# If you want to give a running container a different name
# You can do so by simply renaming it 
# You can rename a running container using the command below
# Replace <container_id> with the container id
# Or use the name instead of the id
# %%bash
docker rename monkey fhtw-hello-app

# Inspect the logs of a running container
# You can inspect the logs of a running container using the command below
# You can always also use the container_id instead of the name
# %%bash
docker logs fhtw-hello-app


# If you want to keep the logs of a running container coming in
# You can follow the logs of a running container using the command below
# You can always also use the container_id instead of the name
# %%bash
docker logs -f fhtw-hello-app 

# After running this command, you should see the logs of the container
# Access the website you should see the logs of the container updating


# Enter the container
# A container is like a small virtual machine with its
# own operatins system, its own file system, network interfaces, and processes
# A running container can also be "entered", meaning, you can also acces that "vm"
# You must run the command below inside a Terminal (not in Jupyter) 
# to enter the container

# %%bash
docker exec -it fhtw-hello-app bash

# If you are inside the container you should see the command prompt changing
# You can browse around the file system, and run commands
# You can exit the container by simply running `exit`


# Now since we already told you that a container is an instance of an image
# you can also run multiple instances of the same image
# Just run the image again (but with a different port, since the current one has been used)
# %%bash
docker run -d -p 8081:8080 fhtw-hello-world

# You can do it as many times as you want
# run as many instances of the same image as you want
# and you can also run different images as well
# but remember that the port should be different
# Now you can access the app using the browser
# by going to localhost:8080 and localhost:8081
# The app is running in different containers, but they are instances of the same image
# and they will be isolated from each other
# The app running on port 8080 will not know about the app running on port 8081
# Now go ahead and list all running containers
# %%bash
docker ps

# You should see all running containers listed
# You can stop all of them using the command below
# %%bash
docker stop $(docker ps -q)


# Maybe you have also noticed that TAG has the value latest
# This actually stands for the `latest` version of the image
# So a tag can be used to specify a version of the image
# For instance you can tag the image with a version number
# You should notice, that the image has the same image id
# but different tags - this is because the image is the same
# we only added a tag to the image
# %%bash
docker tag <image_id> fhtw-hello-world


# %%bash
docker build .



# navigate inside container