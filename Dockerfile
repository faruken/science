FROM python:3.6.0-slim
MAINTAINER faruken <faruken@users.noreply.github.com>
RUN mkdir -p /src && apt-get update && apt-get install -y --no-install-recommends python3-dev supervisor gcc && rm -rf /var/lib/apt/lists/*
ADD . /src
RUN pip3 install --no-cache -r /src/requirements.txt
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENV APP_ENV docker
EXPOSE 4000
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
