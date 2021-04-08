#!/bin/bash
set -v -e

pushd $( dirname $0 )
if [ -f ./env ] ; then
source ./env
fi

# set hostname
sudo hostnamectl set-hostname glasswall

# get source code
cd ~
BRANCH=${BRANCH:-main}
GITHUB_REPOSITORY=${GITHUB_REPOSITORY:-filetrust/cdr-plugin-folder-to-folder}
git clone https://github.com/${GITHUB_REPOSITORY}.git --branch $BRANCH --recursive && cd cdr-plugin-folder-to-folder

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
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# install local docker registry
sudo docker run -d -p 30500:5000 --restart always --name registry registry:2

# build images
cd ~/cdr-plugin-folder-to-folder
cp .env.sample .env
echo "PWD=/home/ubuntu/cdr-plugin-folder-to-folder" >> .env
sudo docker-compose up -d --build

# create script to mount hard disks and upgrade helm chart
tee -a > ~/setup.sh <<EOF
#!/bin/bash
GW_SDK_ADDRESS=\$1
if [[ -z "\$GW_SDK_ADDRESS" ]] ; then
    echo "Please pass glasswall SDK IP address as an argument"
    exit 0
fi
sed -i "s/GW_SDK_ADDRESS=.*/GW_SDK_ADDRESS=\$GW_SDK_ADDRESS/g" .env
cd ~/cdr-plugin-folder-to-folder
sudo docker-compose up -d --build --force

EOF
chmod +x ~/setup.sh

# install vmware tools
sudo apt install open-vm-tools
sudo apt install open-vm-tools-desktop -y

# allow password login (useful when deployed to esxi)
SSH_PASSWORD=${SSH_PASSWORD:-glasswall}
printf "${SSH_PASSWORD}\n${SSH_PASSWORD}" | sudo passwd ubuntu
sudo sed -i "s/.*PasswordAuthentication.*/PasswordAuthentication yes/g" /etc/ssh/sshd_config
sudo service ssh restart
