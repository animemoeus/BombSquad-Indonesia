FROM ubuntu:22.04

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt -y install python3-pip
RUN apt install -y python3.12-dev


ARG BOMBSQUAD_VERSION="1.7.36"

RUN apt-get -y update && \
    apt-get install -y wget
WORKDIR /app

ENV TAR_FILE=BombSquad_Server_Linux_x86_64_${BOMBSQUAD_VERSION}

RUN wget https://files.ballistica.net/bombsquad/builds/$TAR_FILE.tar.gz -O bombsquad.tar.gz && \
    tar -xzf bombsquad.tar.gz --strip-components 1 && \
    rm -f config.yaml # removing default config file in order to put ourselves

CMD ["/app/bombsquad_server"]