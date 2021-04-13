#!/bin/bash
set -e
cd ~/cdr-plugin-folder-to-folder/
git reset --hard && pushd test_data && sudo git reset --hard && popd
git pull
cp .env.sample .env
echo "PWD=/home/ubuntu/cdr-plugin-folder-to-folder" >> .env
source .env
docker-compose build
docker-compose up --force -d