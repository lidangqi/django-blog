FROM nginx:1.17.1

RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker-compose/production/nginx/web.conf /etc/nginx/conf.d/web.conf