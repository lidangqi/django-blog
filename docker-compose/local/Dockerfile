FROM python:3.9.15-alpine3.16

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN apk update
# Pillow dependencies
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
   && apk add gcc python3-dev musl-dev libc-dev libressl-dev libffi-dev openssl-dev cargo \
   && apk add --no-cache mariadb-dev \
   && pip install -r requirements.txt \
   && apk del gcc python3-dev musl-dev libc-dev libressl-dev libffi-dev openssl-dev cargo \
   && rm -rf /var/cache/apk/*

COPY . /app
COPY ./docker-compose/local/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh