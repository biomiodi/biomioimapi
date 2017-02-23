# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:14.04

MAINTAINER Dockerfiles

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && apt-get install -y \
	git \
	python \
	python-dev \
	python-setuptools \
	nginx \
	supervisor \
	sqlite3 \
	libmysqlclient-dev \
	mysql-server \
	nano

#  && rm -rf /var/lib/apt/lists/*

RUN easy_install pip

# RUN /usr/sbin/mysqld & \

#    sleep 10s &&\

#    echo "CREATE DATABASE biomio_db; GRANT ALL ON *.* TO 'biomio_admin'@'%' IDENTIFIED BY 'gate' WITH GRANT OPTION; FLUSH PRIVILEGES; " | mysql

#CMD ["/usr/bin/mysqld_safe"]


# install uwsgi now because it takes a little while
RUN pip install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# ID_RSA
RUN mkdir /root/.ssh
COPY id_rsa /root/.ssh
RUN chmod 600 /root/.ssh/id_rsa
RUN ls -l /root/.ssh


# Clone project from GIT
ENV GITBRANCH development
ENV GITURL "git@bitbucket.org:biomio/biomioimapi.git"

#ARG CACHE_DATE=2016-01-01
RUN ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts


ARG CACHE_DATE=2016-01-01
RUN cd /opt/ && git clone -b $GITBRANCH $GITURL


RUN cd /opt/ && pip install -r biomioimapi/requirements.txt

# add (the rest of) our code
COPY . /opt/biomioimapi/

#RUN echo "service mysql start" >> ~/.bashrc

#RUN echo "mysql -u biomio_admin -pgate biomio_db < /opt/biomioimapi/dump.sql" >> ~/.bashrc


EXPOSE 85
#CMD ["supervisord", "-n"]
