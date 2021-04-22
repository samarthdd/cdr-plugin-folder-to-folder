read -e -p "Enter TFstate S3 bucket name [Default: glasswall-github-actions-terraform-tfstate]: " TFSTATE_BUCKET
TFSTATE_BUCKET=${TFSTATE_BUCKET:-glasswall-github-actions-terraform-tfstate}

read -e -p "Enter TFstate S3 region [Default: eu-west-1]: " TFSTATE_REGION
TFSTATE_REGION=${TFSTATE_REGION:-eu-west-1}

read -e -p "Enter workspace name to use/create [Default: dev]: " WORKSPACE
WORKSPACE=${WORKSPACE:-dev}

terraform init -backend-config="bucket=$TFSTATE_BUCKET" -backend-config="workspace_key_prefix=cdr_plugin_terraform_backend" -backend-config="key=terraform.tfstate" -backend-config="region=$TFSTATE_REGION"
terraform workspace select $WORKSPACE || terraform workspace new $WORKSPACE
terraform plan -var-file tfvars/$WORKSPACE.tfvars
terraform apply -var-file tfvars/$WORKSPACE.tfvars -auto-approve
