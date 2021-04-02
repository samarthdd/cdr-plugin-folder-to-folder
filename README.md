# cdr-plugin-folder-to-folder

# Architecture

![architecture](./diagrams/cdr-plugin-folder-to-folder-architecture.png)

# Setup

- Create virtualenv
- Run `pip install -r common_settings/requirements.txt`

# Services
 
## Pre-Processing

- Run `pytests -v tests`

- Run as Fast API  `uvicorn pre_processing.Pre_Processor:app --reload`

- HD1 --> `test_data/hd1`,  HD2 --> `test_data/hd1`

- Open http://localhost:8000/process


