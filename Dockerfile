#bu mening dockerfile'im

FROM debian:buster-slim

RUN apt-get update && apt-get install -y nginx

FROM nginx:latest
COPY ./README.txt /var/www/html/README.txt

CMD ["nginx", "-g", "daemon off;"]



