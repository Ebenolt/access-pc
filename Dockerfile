FROM debian

WORKDIR /home

ENV SHELL=/bin/sh

RUN ["apt-get", "update"]

RUN ["apt-get", "install", "-y", "python3", "python3-pip", "default-libmysqlclient-dev", "pipenv"]

COPY . /home/access-pc

WORKDIR /home/access-pc

RUN ["pipenv", "install"]

ENTRYPOINT ["/bin/sh", "/home/access-pc/res/docker_start.sh"]
