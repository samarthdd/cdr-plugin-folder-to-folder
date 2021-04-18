#!/bin/bash
set -e

# 1. clone or download the files
sudo rm -rf test/scenario-data-sets/
mkdir -p test/scenario-data-sets/{hd2,hd3}
pushd test/scenario-data-sets/ && git clone https://github.com/k8-proxy/data-sets.git && popd
hd1=test/scenario-data-sets/data-sets
hd2=test/scenario-data-sets/hd2
hd3=test/scenario-data-sets/hd3

# 2. update .env file with host folders
sed -i "s|HOST_HD1_LOCATION=.*|HOST_HD1_LOCATION=${hd1}|" .env.sample
sed -i "s|HOST_HD2_LOCATION=.*|HOST_HD2_LOCATION=$hd2|g" .env.sample
sed -i "s|HOST_HD3_LOCATION=.*|HOST_HD3_LOCATION=$hd3|g" .env.sample

# 3. start docker compose
docker-compose build
source .env.sample
docker-compose up -d --force
sleep 5s

# 4. run pre-processing
base_url=localhost:8880
curl --location --request GET "http://${base_url}/health"
time curl --location --request POST "http://${base_url}/pre-processor/pre-process"

# 5. run processing
time curl --location --request POST "http://${base_url}/processing/start"


cat $hd2/status/status.json 
files_to_process=$(cat $hd2/status/status.json | jq -r ".files_to_process")
failed=$(cat $hd2/status/status.json | jq -r ".failed")
completed=$(cat $hd2/status/status.json | jq -r ".completed")

# 6. clear data
curl --location --request POST "http://${base_url}/pre-processor/clear-data-and-status"

