#FROM    python:3.9.3-alpine3.12
#       todo: refacor to use alpine version (above). The version below was needed to use the python pstools
#             but it increases the docker image size quite considerably
FROM    python:3.9.3

RUN     apt update && \
        apt install -y bash git

WORKDIR /app
COPY    cdr_plugin_folder_to_folder/requirements.txt .
RUN     pip install -r requirements.txt
ADD     cdr_plugin_folder_to_folder ./cdr_plugin_folder_to_folder
COPY    .env.sample ./cdr_plugin_folder_to_folder/.env
ENV     PYTHONPATH=.
CMD     python cdr_plugin_folder_to_folder/api/Server.py
EXPOSE  8880