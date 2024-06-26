FROM ubuntu:22.04

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y
RUN apt install python3-pip -y
RUN apt install python3.12-dev -y

WORKDIR /app
COPY . /app

CMD ["/app/bombsquad_server"]