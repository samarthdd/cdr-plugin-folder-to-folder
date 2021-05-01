cd docs
docker build -t cdr_plugin_folder_to_folder_docs .
docker  run --rm -it -p 1313:1313          \
        -v $(pwd)/site:/src/site                \
        cdr_plugin_folder_to_folder_docs
