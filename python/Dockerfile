FROM ubuntu:20.04

# Create app directory
WORKDIR .

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev curl

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt install python3 python3-dev python3-distutils
RUN python3 get-pip.py
RUN pip3 install flask flask_cors multiprocess

# RUN python3 -V
# RUN pip3 install importlib==1.0.4 # don't need if python versoin above 3.6

# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "python3", "oo_app.py" ]