# cdr-plugin-folder-to-folder

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

![image](https://user-images.githubusercontent.com/70108899/113400135-a314d000-93a1-11eb-8b5f-5d9fb3679264.png)

## Data mapping

![image](https://user-images.githubusercontent.com/70108899/113400135-a314d000-93a1-11eb-8b5f-5d9fb3679264.png)

## Usage

- Set minio and jupyter notebook password 
    ```
     export ACCESS_TOKEN=
  
   ```
  
- Run `docker-compose up`

## Services

### Fast API

- Open `http:0.0.0.0:8880`
- Endpoints

| API Endpoint | Method | Description | 
|------|---------|---------    |
| /    |  GET |  Home Screen |
| /pre-process    | GET |  Pre processing of file from HD1 to HD2      |
| /loop   | GET | Processing of HD2 files and storing result in HD3 |

## Jupyter Notebook
- Open `http:0.0.0.0:8888/`
- Use `access_token` as password

## Minio
- Open `http:0.0.0.0:9000/`
- Use `access_token` as password

## Elastic Search
- Open `http:0.0.0.0:5601/`
- Use `access_token` as password

## Kibana
- Open `http:0.0.0.0:9200/`
- Use `access_token` as password

