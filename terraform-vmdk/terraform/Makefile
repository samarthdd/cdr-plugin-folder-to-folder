.DEFAULT-GOAL: default

export PWD = $(shell pwd)
export PATH = $(PWD)/bin:$(shell echo $$PATH)

.PHONY: default
default:

.PHONY: init
init:
	terraform init -upgrade

.PHONY: apply
apply:
	terraform apply

.PHONY: destroy
destroy:
	terraform destroy

.PHONY: plan
plan:
	terraform plan
