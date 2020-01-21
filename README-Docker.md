# Docker

This repository contains a Dockerfile to run the Python-based Bunq tinker code in Docker. This file can be used to create a Docker image from this repository and run the code within a Docker container. The main benefit is that the results are reproducible, this reduces the time needed to hunt for bugs.

## Prerequisites

- You should have Docker installed on your host system.
- Instructions to install Docker can be found [here](./README-Docker-Installation.md).

## Usage

- Once Docker is installed, clone this repository to a directory of choice.
- Build the image with `docker build -t bunq-python-tinker-image .`
- Create a new container and run the image within that container.
  - **TEMPORARY CONTAINER** &mdash; `docker run --rm --name bunq-python-tinker-container -it bunq-python-tinker-image` will create and run a _temporary container_, i.e. it gets removed after it exits.
  - **PERMANENT CONTAINER** &mdash; `docker run --name bunq-python-tinker-container -it bunq-python-tinker-image` will create and run a _persistent container_, i.e. it remembers all changes and could be used for production.
- Try to run `tinker/user_overview.py`. It will automatically create a new sandbox account.

## Removal

- To remove the container: `docker container rm bunq-python-tinker-container`
- To remove the image: `docker image rm bunq-python-tinker-image`

### Dangling containers and images

Sometimes during development you choose to create multiple containers using different names. That's very useful when tinkering, but could also result in having containers you didn't know you still had.

- To list all containers and images
  - `docker container ls --all`
  - `docker image ls --all`
- To remove a particular container or image
  - `docker container rm <CONTAINER ID>`
  - `docker image rm <IMAGE ID>`
- To remove dangling containers and images (dangerous, it removes all stopped containers and unused images from your system, including your own ones).
  - `docker container prune`
  - `docker image prune`

