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


=======
**Repo Workflows**

![](https://github.com/filetrust/cdr-plugin-folder-to-folder/actions/workflows/run-tests.yml/badge.svg)

## Project 

- This project aims to create a deployment that is able to process **1TB** of unique unsafe files, shared on the harddrive. 
- Implementation should pick up these files and process them via Rebuild engine in a deployment based on 2 ESXi servers.

## Arhitecture 

- Workflow cluster
- Worker cluster
- Load balancer
- Monitoring
- 3 Harddisks (source, evidence and target)


## Flow diagram

![defense_school_revised](https://user-images.githubusercontent.com/70108899/113388987-87a0c980-938f-11eb-9fab-f397383f7c95.jpg)

## Data mapping

![image](https://user-images.githubusercontent.com/70108899/113400135-a314d000-93a1-11eb-8b5f-5d9fb3679264.png)
