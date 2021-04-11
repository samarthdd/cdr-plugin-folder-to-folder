.DEFAULT-GOAL: default

export PWD = $(shell pwd)
export PATH = $(PWD)/bin:$(shell echo $$PATH)

.PHONY: default
default: copy build clean

.PHONY: copy
copy:
	@cd .. && git archive --format tar --output '$(PWD)/terraform.tar' HEAD terraform 
	@tar -xpf terraform.tar terraform

.PHONY: build
build:
	@chmod 0755 build.sh && \
	sudo alpine-make-vm-image -f vmdk -c alpine.vmdk build.sh

.PHONY: clean
clean:
	@rm -rf terraform terraform.tar