Terraform for VMWare
===

- [Terraform for VMWare](#terraform-for-vmware)
  - [1. Configuration](#1-configuration)
  - [2. Apply](#2-apply)

## 1. Configuration

Make a copy of *secret.auto.tfvars.example* and place your credentials.

```shell
cp -pv secret.auto.tfvars.example secret.auto.tfvars
"${VISUAL}" secret.auto.tfvars
```

Now, we have to initialize Terraform.

```shell
terraform init
```

Configure VMs using variables. See an example at *default.auto.tfvars*.

## 2. Apply

```shell
terraform apply
```