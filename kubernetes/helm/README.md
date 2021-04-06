# Deploy CDR plugin folder to folder API to kubernetes

## Clone the repository
```
git clone --single-branch -b main https://github.com/filetrust/cdr-plugin-folder-to-folder.git
cd cdr-plugin-folder-to-folder
```

## Minimalist deployment without SSL. API can be accessed only on port 80 (only for development purpose)

The paths where host directories are mounted in the container can be controlled by setting values - `application.cdrplugin.env.HD1_LOCATION`, `application.cdrplugin.env.HD2_LOCATION`, `application.cdrplugin.env.HD3_LOCATION`

The paths of host directories which needs to be mounted can be controlled by setting values - `hostPath.hd1.path`, `hostPath.hd2.path`, `hostPath.hd3.path`

```
helm upgrade --install cdr-plugin-f2f \
  --set image.cdrplugin.repository=<docker-repository> \
  --set image.cdrplugin.tag=<image_name:image_tag>  \
  --set application.cdrplugin.env.HD1_LOCATION="/mnt/hd1" \
  --set application.cdrplugin.env.HD2_LOCATION="/mnt/hd2" \
  --set application.cdrplugin.env.HD3_LOCATION="/mnt/hd3" \
  --set ingress.tls.enabled=false \
  --atomic kubernetes/helm/chart/
```

**example:**
```
helm upgrade --install cdr-plugin-f2f \
  --set image.cdrplugin.repository=pranaysahith/cdr_plugin_folder_to_folder \
  --set image.cdrplugin.tag=0.0.2  \
  --set application.cdrplugin.env.HD1_LOCATION="/mnt/hd1" \
  --set application.cdrplugin.env.HD2_LOCATION="/mnt/hd2" \
  --set application.cdrplugin.env.HD3_LOCATION="/mnt/hd3" \
  --set service.cdrplugin.url="cdrplugin-dev01.glasswall-icap.com"
  --set ingress.tls.enabled=false \
  --atomic kubernetes/helm/chart/
```


## Deployment using SSL certificates

### Generate self signed certificates if necessary
```
pushd infra/packer/setup/ssl/
# update DNS.1 value in openssl.cnf with the desired DNS name
chmod +x gencert.sh
bash gencert.sh
popd
cp infra/packer/setup/ssl/server.key infra/packer/setup/ssl/server.crt infra/packer/setup/ssl/ca.pem .
```

```
# make sure server.key, server.ctr and ca.pem files are in current folder
key=$(cat ./server.key | base64 | tr -d '\n')
crt=$(cat ./server.crt ./ca.pem | base64 | tr -d '\n')

helm upgrade --install cdr-plugin-f2f \
  --set image.cdrplugin.repository=<docker-repository> \
  --set image.cdrplugin.tag=<image_name:image_tag> \
  --set application.cdrplugin.env.HD1_LOCATION="/mnt/hd1" \
  --set application.cdrplugin.env.HD2_LOCATION="/mnt/hd2" \
  --set application.cdrplugin.env.HD3_LOCATION="/mnt/hd3" \
  --set service.cdrplugin.url="<Domain_name>" \
  --set ingress.tls.crt=$crt \
  --set ingress.tls.key=$key \
  --atomic kubernetes/helm/chart/
```

### Validate deployment
Once the helm chart is delployed run below commands to validate if the resources are deployed:
```
kubectl get pods
kubectl get svc
kubectl get ingress
```

### Access the API
Update the global DNS server such as Route53 or the `hosts` file in local machine with the IP address of ingress for the domain used during deployment.
Access the API at http(s)://<domain_name>/.
