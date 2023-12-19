FROM python:3.11.4-slim-bullseye
LABEL authors="Chris Chen"


RUN apt-get update -y \
    && apt-get -y install nginx

COPY ./nginx/ /etc/nginx/conf.d/
COPY . /app/

WORKDIR /app
RUN pip install -r requirements.txt \
    && chown -R www-data /app/frontend/build

EXPOSE 9310
VOLUME [ "/app/config" ]

ENTRYPOINT ["./entrypoint"]