# S3 Mount

- Download rclone
```
curl https://rclone.org/install.sh | sudo bash
```
- Run 
`rclone config
`
- Enter below values 

```
    n/s/q>                 -  n 
    name>                  -  <Name>
    Storage                - 4
    provider               - 1
    env_auth               - 1 and give aws access key and secret key
    region                 - <blank>
    endpoint               - <blank>
    location_constraint    - <blank>
    acl                    - 2 ( depends on use case )
    server_side_encryption - 2
    sse_kms_key_id         - 2
    storage_class          - 2 ( depends on use case )
    Edit advanced config?  - n
    <y/e/d>                 - n

```

- Verify s3 is connected by listing all buckets `rclone lsd <Name>:`  
  Example   `rclone lsd remote_s3:`
  
- Copy 

    ```
    rclone copy <Name>:<Bucket_Name>/<folder> <local_destination_location>
  ```
  
- Mount 

    ```
    rclone mount <Name>:<Bucket_Name>/<folder> <local_destination_location>  --daemon 
   ```
- For more details Follow doc `https://rclone.org/s3/`

