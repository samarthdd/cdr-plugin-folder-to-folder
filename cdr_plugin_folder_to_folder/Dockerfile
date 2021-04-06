FROM    python:3.9.3-alpine3.12

RUN     apk update && apk upgrade && \
        apk add --no-cache bash git openssh
WORKDIR /app
COPY    requirements.txt .
RUN     pip install -r requirements.txt
COPY    . .
ENV     PYTHONPATH=.
CMD     python cdr_plugin_folder_to_folder/api/Server.py
EXPOSE 8880