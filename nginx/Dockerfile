FROM nginx:1.25.4

RUN mkdir /ssl
RUN mkdir /home/static
COPY ./nginx.conf /etc/nginx/nginx.conf
# COPY ./conf.d /etc/nginx/conf.d
COPY ./static /home/static
COPY ./ssl /ssl
