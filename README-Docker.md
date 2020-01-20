# Docker

This repository contains a Dockerfile to run the Python SDK in Docker.

## Prerequisites

- You should have Docker installed on your host system.
- Instructions to install Docker can be found [here](./README-Docker-Installation.md).

## Usage

- Once Docker is installed, clone this repository to a directory of choice.
- Build the image with `docker build -t bunq-python-sdk .`
- Create a new container and run the image within that container.
  - **TEMPORARY CONTAINER** &mdash; `docker run --rm --name bunq-python-container -it bunq-python-sdk` will create and run a _temporary container_, i.e. it gets removed after it exits.
  - **PERMANENT CONTAINER** &mdash; `docker run --name bunq-python-container -it bunq-python-sdk` will create and run a _persistent container_, i.e. it remembers all changes and could be used for production.
- Try to run `tinker/user_overview.py`. It will automatically create a new sandbox account.

## Removal

- To remove the container: `docker container rm bunq-python-container`
- To remove the image: `docker image rm bunq-python-sdk`

### Full removal

- To remove dangling containers and images (dangerous, it removes all stopped containers and images from your system, including your own ones).
  - `docker container prune`
  - `docker image prune`

