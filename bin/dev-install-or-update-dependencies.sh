echo "\n\n**** Installing or Updating python dependencies *****\n\n"

# todo: add check for use of virtual environment and create one if needed
pip install -r cdr_plugin_folder_to_folder/requirements.txt
pip install -e .