FROM debian:10.6

ENV WORKDIR='/app'


COPY . /app
WORKDIR $WORKDIR

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-dev python3-pip vim && \
    pip3 install -r requirements.txt

CMD python3 $WORKDIR/code/Bot.py
