FROM debian

WORKDIR /home

COPY deploy.sh .

RUN ["chmod", "+x", "/home/deploy.sh"]

RUN ["/bin/sh", "-c", "/home/deploy.sh"]

RUN ["pipenv", "shell", "--fancy"]

RUN ["chmod", "+x", "/home/access-pc/start.sh"]

RUN ["/bin/sh", "-c" ,"home/access-pc/start.sh"]
