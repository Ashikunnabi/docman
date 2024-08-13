FROM nginx:1.21.3-alpine

RUN mkdir /etc/nginx/sites-available /etc/nginx/sites-enabled

COPY ./docker/nginx/inventory /etc/nginx/sites-available/

RUN rm /etc/nginx/nginx.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

RUN  ln -s /etc/nginx/sites-available/inventory /etc/nginx/sites-enabled/
