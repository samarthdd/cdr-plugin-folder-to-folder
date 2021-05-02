cd jupyter
docker build -t cdr_plugin_folder_to_folder_notebooks .

#docker run --rm -it -p 8888:8888  cdr_plugin_folder_to_folder
docker run --rm -it -p 8888:8888 -p 8866:8866            \
        -v $(pwd)/notebooks:/home/jovyan/work            \
        -v $(pwd)/../test_data:/home/jovyan/test_data    \
        cdr_plugin_folder_to_folder_notebooks