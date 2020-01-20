# Docker Installation Guide

This guide explains how to install Docker on your host system.

## Ubuntu

First thing you'll need to do is to install Docker

````sh
sudo apt install docker.io
````

Then, add your current user to the `docker` group

```sh
sudo gpasswd -a $USER docker && newgrp docker
```

After that, try to run the `hello-world` docker-image to test if all permissions are set up correctly and your Docker installation works

````sh
docker run hello-world
````

Docker should begin downloading the `hello-world` image and run it immediately, and shows the following output:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

(...)
```

Done.

## macOS

- To do.

## Windows

- To do.