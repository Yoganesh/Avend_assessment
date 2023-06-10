FROM python:3.8
WORKDIR /usr/src/app
COPY . .
# RUN apt-get -y install mysql-server python-mysqldb
RUN pip install -r requirements.txt
RUN pip install pydantic[email]
EXPOSE 6655
CMD ["./run.sh"]

# FROM ubuntu:20.04
#
# RUN apt-get update
# RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip
# RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server python3-mysqldb
#
# WORKDIR /usr/src/app
# COPY . .
# RUN pip install -r requirements.txt
# RUN pip install pydantic[email]
#
# EXPOSE 6655
# CMD ["./run.sh"]