FROM        --platform=$TARGETOS/$TARGETARCH selenium/standalone-chrome

LABEL       author="pintang" maintainer="pintang"

RUN         sudo apt update \
            && sudo apt -y install git gcc g++ ca-certificates dnsutils curl iproute2 ffmpeg procps tini \
            && sudo useradd -m -d /home/container container
RUN sudo apt-get install -y software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt-get install -y python3.8 python3-pip
RUN sudo apt-get install -y python3.8-distutils
RUN sudo apt-get install -y python3-apt

# Update symlink to point to latest
RUN sudo rm /usr/bin/python3 && sudo ln -s /usr/bin/python3.8 /usr/bin/python3
RUN sudo apt install python-is-python3
RUN python --version
RUN pip --version


USER        container
ENV         USER=container HOME=/home/container
WORKDIR     /home/container

STOPSIGNAL SIGINT

COPY        --chown=container:container ./../entrypoint.sh /entrypoint.sh
RUN         chmod +x /entrypoint.sh
ENTRYPOINT    ["/usr/bin/tini", "-g", "--"]
CMD         ["/entrypoint.sh"]
