.DEFAULT-GOAL: default

export PWD = $(shell pwd)
export PATH = $(PWD)/bin:$(shell echo $$PATH)

.PHONY: default
default: build

.PHONY: build
build:
	@chmod 0755 build.sh && \
	sudo alpine-make-vm-image -f vmdk -c alpine.vmdk build.sh
