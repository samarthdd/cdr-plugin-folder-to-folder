Terraform for OVA/OVF ESXi deployment
===

- [Terraform for OVA/OVF ESXi deployment](#terraform-for-ovaovf-esxi-deployment)
  - [1. Requirements](#1-requirements)
  - [2. Configuration](#2-configuration)
  - [3. Apply](#3-apply)


## 1. Requirements

Install [OVF tools](https://my.vmware.com/group/vmware/downloads/details?downloadGroup=OVFTOOL441&productId=955). We have downloaded it for Linux x64 at ./artifacts folder.

```shell
sudo bash ./VMware-ovftool-4.4.1-16812187-lin.x86_64.bundle
```

## 2. Configuration

Make a copy of *secret.auto.tfvars.example* and place your credentials.

```shell
cp -pv secret.auto.tfvars.example secret.auto.tfvars
"${VISUAL}" secret.auto.tfvars
```

Now, we have to initialize Terraform.

```shell
terraform init
```

Configure VMs using variables. See an example at *default.auto.tfvars*. See the list of variables in *variables.tf* or refer to the table below.

|         Variable | Description                      |
| ---------------: | -------------------------------- |
| esxi_credentials | ESXi connection details          |
|   instance_count | Count of instances               |
|      name_prefix | Name prefix for the instances    |
|        datastore | Datastore name                   |
|       ovf_source | Local path or URL to OVF         |
|          network | Network name                     |
|       vcpu_count | Count of vCPU per instance       |
|       memory_mib | Count of RAM per instance in MiB |
|    auto_power_on | Will power on instances if true  |
|   boot_disk_size | HDD size of GiB                  |


## 3. Apply

Now you can apply the changes.

```shell
terraform apply
```
