FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  && apk add gcc python3-dev musl-dev libc-dev libressl-dev libffi-dev openssl-dev cargo \
  && apk add --no-cache mariadb-dev
WORKDIR /app

RUN pip install pipenv -i https://pypi.douban.com/simple

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile
RUN apk del gcc python3-dev musl-dev libressl-dev libffi-dev openssl-dev cargo && rm -rf /var/cache/apk/*

COPY ./docker-compose/local/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh