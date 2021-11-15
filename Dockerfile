FROM debian

WORKDIR /home

ENV SHELL=/bin/sh

RUN ["apt-get", "update"]

RUN ["apt-get", "install", "-y", "git", "python3", "python3-pip", "default-libmysqlclient-dev", "pipenv"]

RUN ["git", "clone", "https://github.com/Ebenolt/access-pc"]

WORKDIR /home/access-pc

RUN ["pipenv", "install"]

ENTRYPOINT ["pipenv", "run", "/bin/sh" ,"/home/access-pc/start.sh"]