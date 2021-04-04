# Ubuntu Packer template for AWS AMI

## Overview

Packer template to build Ubuntu VM with the following configuration

- Hostname: **glasswall**

- Username: **ubuntu**

- sudo enabled for user **ubuntu** , with no password prompt

## Build requirements

### Build machine

the machine running this packer template must have the following installed

- packer

### Usage

- Prepare the project by running the following
  
  - ```bash
    git clone --single-branch -b main https://github.com/filetrust/cdr-plugin-folder-to-folder.git
    cd infra/packer/
    cp aws-vars.json.example vars.json
    ```
    
    ```bash
    nano vars.json # then tweak parameters as needed, and exit
    ```

- Start the build
  
  ```bash
  PACKER_LOG=1 PACKER_LOG_PATH=packer.log packer build -on-error=ask -var-file=vars.json aws-ami.json
  ```

- You should be able to find the AMI in the AWS account and the region used in vars.json using the AMI ID

