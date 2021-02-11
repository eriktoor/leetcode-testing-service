FROM ubuntu:18.04

# Create app directory
WORKDIR .

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev curl

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

RUN apt-get install -y python3-distutils python3-apt

RUN pip3 install flask flask_cors multiprocess importlib
# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "python3", "oo_app.js" ]