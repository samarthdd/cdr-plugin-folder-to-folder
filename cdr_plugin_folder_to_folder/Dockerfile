FROM    python:3.9.3-alpine3.12

RUN     apk update && apk upgrade && \
        apk add --no-cache bash git openssh

COPY    requirements.txt /app/requirements.txt
WORKDIR /app
RUN     pip install -r requirements.txt
COPY    . /app/cdr_plugin_folder_to_folder
ENV     PYTHONPATH=.
CMD     python cdr_plugin_folder_to_folder/api/Server.py
#CMD     ls -la