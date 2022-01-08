#docker build -t explosion-diffuser .
#docker run --name explosion-diffuser -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY explosion-diffuser
FROM ubuntu:latest
RUN apt-get -y update && DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip python3-dev python3-tk libfreetype6-dev libportmidi-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev && rm -rf /var/lib/apt/lists/*
COPY . /usr/src/explosion-diffuser
WORKDIR /usr/src/explosion-diffuser
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["src/main.py"]
