FROM ubuntu:18.04

# Create app directory
WORKDIR .

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN pip install -r requirements.txt
# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "python3", "oo_app.js" ]