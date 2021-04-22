![OvaToEsxiDeploy](https://user-images.githubusercontent.com/78961055/114981290-61a91800-9eab-11eb-82a2-c628805a8f4c.png)

```shell
Download SDK, Workflow and Installer/Monitor(Glasswall Desktop) OVAs from AWS S3 bucket to the User computer.
Connect to ESXi-01 from User Computer and manually import the Installer ova and start the Installer VM instance.
Copy the SDK, Workflow OVAs and Terraform code from User Computer to the datastore of ESXi-01 and mount the datastore to Installer VM Instance.
Run the Terraform from Installer VM Instance.
Validate the SDK and Workflow VM Instances created in respective ESXi.
```




Terraform for OVA/OVF ESXi deployment
===

- [Terraform for OVA/OVF ESXi deployment](#terraform-for-ovaovf-esxi-deployment)
  - [1. OVA/OVF](#1-ovaovf)
    - [1.1. Requirements](#11-requirements)
    - [1.2. Configuration](#12-configuration)
    - [1.3. Terraform_apply](#13-Terraform_apply)
  - [2. VMDK](#2-vmdk)
    - [2.1. Configuration](#21-configuration)
  - [3. Apply](#3-apply)

## 1. OVA/OVF

> See an example in \infra\terraform\esxi\tfvars\secret.auto.tfvars.example

### 1.1. Requirements

Install [OVF tools](https://my.vmware.com/group/vmware/downloads/details?downloadGroup=OVFTOOL441&productId=955). We have downloaded it for Linux x64 at ./artifacts folder.

```shell
sudo bash ./VMware-ovftool-4.4.1-16812187-lin.x86_64.bundle
```

### 1.2. Configuration

Navigate to tfvars folder 
```shell
cd infra/terraform/esxi/tfvars
```
Make a copy of *secret.auto.tfvars.example* and place your credentials.
```shell
cp secret.auto.tfvars.example secret.auto.tfvars
```
update details as require in secret.auto.tfvars

Now, we have to initialize Terraform.

Configure VMs details using secret.auto.tfvars. See an example at *infra/terraform/esxi/tfvars/secret.auto.tfvars.example*. See the list of variables below.

|        Variable | Description                      |
| --------------: | -------------------------------- |
| ssh_credentials | ESXi SSH connection details      |
|  instance_count | Count of instances               |
|     name_prefix | Name prefix for the instances    |
|       datastore | Datastore name                   |
|      ovf_source | Local path or URL to OVF         |
|         network | Network name                     |
|      vcpu_count | Count of vCPU per instance       |
|      memory_mib | Count of RAM per instance in MiB |
|   auto_power_on | Will power on instances if true  |
|  boot_disk_size | HDD size of GiB                  |


### 1.3. Terraform_apply

once the value is updated in secret.auto.tfvars run

```shell
terraform init -upgrade
```
run terraform plan to validate the code

```shell
terraform plan
```
run terraform apply to deploy the VMs

```shell
terraform apply
```

## 2. VMDK

> See an example in vmdk.tf.example

### 2.1. Configuration

Make a copy of *secret.auto.tfvars.example* and place your credentials.

```shell
cp -pv secret.auto.tfvars.example secret.auto.tfvars
"${VISUAL}" secret.auto.tfvars
```

Now, we have to initialize Terraform.

```shell
terraform init -upgrade
```

Configure VMs modules using variables from esxi-instance module. See an example at *esxi-instance/variables.tf*. See the list of variables in *variables.tf* or refer to the table below.

|        Variable | Description                      |
| --------------: | -------------------------------- |
| ssh_credentials | ESXi SSH connection details      |
|  instance_count | Count of instances               |
|     name_prefix | Name prefix for the instances    |
|       datastore | Datastore name                   |
|            vmdk | Path to vmdk in datastore        |
|         network | Network name                     |
|             cpu | Count of vCPU per instance       |
|             ram | Count of RAM per instance in MiB |

## 3. Apply

Now you can apply the changes.

```shell
terraform apply
```
