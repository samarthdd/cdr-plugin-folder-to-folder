FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN apk --no-cache add git
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
RUN pip3 install -e .
EXPOSE 80

ENTRYPOINT ["python3"]
CMD ["cdr_plugin_folder_to_folder/processing/main.py"]
