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


![defense_school_revised](https://user-images.githubusercontent.com/70108899/113388987-87a0c980-938f-11eb-9fab-f397383f7c95.jpg)

## Flow diagram

![image](https://user-images.githubusercontent.com/70108899/113400135-a314d000-93a1-11eb-8b5f-5d9fb3679264.png)

## Data mapping
