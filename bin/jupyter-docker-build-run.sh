cd notebooks
docker build -t cdr_plugin_folder_to_folder_notebooks .

#docker run --rm -it -p 8888:8888  cdr_plugin_folder_to_folder
docker run --rm -it -p 8888:8888 -v $(PWD):/home/jovyan cdr_plugin_folder_to_folder_notebooks