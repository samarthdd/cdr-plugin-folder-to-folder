cd cdr_plugin_folder_to_folder
docker build -t cdr_plugin_folder_to_folder .

#docker run --rm -it -p 8888:8888  cdr_plugin_folder_to_folder
docker run --rm -it -p 8888:8888 -v $(PWD):/app/cdr_plugin_folder_to_folder cdr_plugin_folder_to_folder