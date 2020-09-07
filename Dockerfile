from ubuntu:bionic

# Install the dependencies
RUN apt update && \
    apt install -y curl \ 
                   git \
                   python3 \
                   python-pip \
                   python3-distutils \
                   qrencode \
                   jq \
                   locales

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# Install pipenv
RUN pip install pipenv

# Set up user and home directories
SHELL ["/bin/bash", "-c"]
RUN useradd -s /bin/bash bunq
RUN mkdir -p /home/bunq && chown -R bunq: /home/bunq

USER bunq
WORKDIR /home/bunq
COPY --chown=bunq:bunq . .

# Remove -W ignore
RUN sed -i -e 's/ -W ignore//' ./tinker/**/*.py

# Remove Empty Directory assert
RUN sed -i -e 's/^assertIsRanInEmptyDirectory$//' ./setup.sh

# Remove Git clone
RUN sed -i -e 's/^cloneTinkerPython$//' ./setup.sh

# Run the setup script
RUN ["/bin/bash", "-c", "bash ./setup.sh"]

CMD ["/bin/bash"]
