#!/bin/bash
set -v -e

pushd $( dirname $0 )
if [ -f ./env ] ; then
source ./env
fi

# set hostname
sudo hostnamectl set-hostname glasswall

# install k3s
curl -sfL https://get.k3s.io | sh -
mkdir -p ~/.kube && sudo install -T /etc/rancher/k3s/k3s.yaml ~/.kube/config -m 600 -o $USER

# install kubectl and helm
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
echo "Done installing kubectl"

curl -sfL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
echo "Done installing helm"

# get source code
cd ~
BRANCH=${BRANCH:-main}
git clone https://github.com/pranaysahith/cdr-plugin-folder-to-folder.git --branch $BRANCH && cd cdr-plugin-folder-to-folder

# build docker images
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install docker-ce docker-ce-cli containerd.io -y

# install local docker registry
sudo docker run -d -p 30500:5000 --restart always --name registry registry:2

# build images
cd ~/cdr_plugin_folder_to_folder
sudo docker build cdr_plugin_folder_to_folder -f Dockerfile -t localhost:30500/cdr-plugin-folder-to-folder
sudo docker push localhost:30500/cdr-plugin-folder-to-folder

# install cdr plugin folder to folder API helm charts
GW_SDK_PORT=${GW_SDK_PORT-1346}
helm upgrade --install cdr-plugin-f2f  \
    --set image.cdrplugin.repository=localhost:30500/cdr-plugin-folder-to-folder \
    --set image.cdrplugin.tag=latest \
    --set application.cdrplugin.env.HD1_LOCATION="/mnt/hd1" \
    --set application.cdrplugin.env.HD2_LOCATION="/mnt/hd2" \
    --set application.cdrplugin.env.HD3_LOCATION="/mnt/hd3" \
    --set image.cdrplugin.env.GW_SDK_ADDRESS=$GW_SDK_ADDRESS \
    --set ingress.tls.enabled=false \
    --atomic kubernetes/helm/chart/

# create script to mount hard disks and upgrade helm chart
tee -a > ~/setup.sh <<EOF
#!/bin/bash
GW_SDK_ADDRESS=$1
if [[ -z "$GW_SDK_ADDRESS" ]] ; then
    echo "Please pass glasswall SDK IP address as an argument"
    exit 0
fi
GW_SDK_PORT=${2-1346}
mkdir -p /mnt/hd1 /mnt/hd2 /mnt/hd3

helm upgrade --install cdr-plugin-f2f \
  --set image.cdrplugin.repository=localhost:30500/cdr-plugin-folder-to-folder \
  --set ingress.tls.enabled=false \
  --set image.cdrplugin.env.HD1_LOCATION="/mnt/hd1" \
  --set image.cdrplugin.env.HD2_LOCATION="/mnt/hd2" \
  --set image.cdrplugin.env.HD3_LOCATION="/mnt/hd3" \
  --set image.cdrplugin.env.GW_SDK_ADDRESS=$GW_SDK_ADDRESS \
  --set image.cdrplugin.env.GW_SDK_PORT=$GW_SDK_PORT \
  --atomic kubernetes/helm/chart/

EOF
chmod +x ~/setup.sh

# allow password login (useful when deployed to esxi)
SSH_PASSWORD=${SSH_PASSWORD:-glasswall}
printf "${SSH_PASSWORD}\n${SSH_PASSWORD}" | sudo passwd ubuntu
sudo sed -i "s/.*PasswordAuthentication.*/PasswordAuthentication yes/g" /etc/ssh/sshd_config
sudo service ssh restart
