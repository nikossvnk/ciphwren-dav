FROM python:3.13

ENV CIPHWREN_DATA_DIR "/data"
ENV CIPHWREN_SERVER_HOSTS "0.0.0.0:37358,[::]:37358"

# Make this file a build dep for the next steps
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /app
RUN pip install /app

RUN set -ex ;\
        useradd ciphwren ;\
        mkdir -p /data ;\
        chown -R ciphwren: /data

VOLUME /data
EXPOSE 37358

USER ciphwren

ENTRYPOINT ["ciphwren-dav"]
