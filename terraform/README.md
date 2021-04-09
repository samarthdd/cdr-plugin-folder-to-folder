Terraform for OVA/OVF ESXi deployment
===

- [Terraform for OVA/OVF ESXi deployment](#terraform-for-ovaovf-esxi-deployment)
  - [1. OVA/OVF](#1-ovaovf)
    - [1.1. Requirements](#11-requirements)
    - [1.2. Configuration](#12-configuration)
  - [2. VMDK](#2-vmdk)
    - [2.1. Configuration](#21-configuration)
  - [3. Apply](#3-apply)

## 1. OVA/OVF

> See an example in ova.tf.example

### 1.1. Requirements

Install [OVF tools](https://my.vmware.com/group/vmware/downloads/details?downloadGroup=OVFTOOL441&productId=955). We have downloaded it for Linux x64 at ./artifacts folder.

```shell
sudo bash ./VMware-ovftool-4.4.1-16812187-lin.x86_64.bundle
```

### 1.2. Configuration

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
|      ovf_source | Local path or URL to OVF         |
|         network | Network name                     |
|      vcpu_count | Count of vCPU per instance       |
|      memory_mib | Count of RAM per instance in MiB |
|   auto_power_on | Will power on instances if true  |
|  boot_disk_size | HDD size of GiB                  |


## 2. VMDK

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
