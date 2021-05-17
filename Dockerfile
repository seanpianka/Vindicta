FROM python:3.6-slim-stretch

# Python + Deps
COPY requirements.txt /tmp/requirements.txt
RUN apt update
RUN apt install -y \
        build-essential \
        make \
        gcc \
        locales
RUN pip install --requirement /tmp/requirements.txt
RUN dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8
ENV LC_ALL C.UTF-8

# Selenium dependencies
RUN apt update -y && apt install -y wget curl unzip libgconf-2-4
RUN apt update -y && apt install -y chromium xvfb python3 python3-pip 
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Clean-up
RUN rm -r /root/.cache/pip
RUN apt remove -y --purge libgdal-dev make gcc build-essential
RUN apt autoremove -y
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY vindicta.py .

# Set display port and dbus env to avoid hanging
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null
# Bash script to invoke xvfb, any preliminary commands, then invoke project
COPY run.sh .
CMD /bin/bash run.sh
