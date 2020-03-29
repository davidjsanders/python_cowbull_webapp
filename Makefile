ifndef BUILD_NUMBER
  override BUILD_NUMBER := 7
endif

ifndef COWBULL_PORT
  override COWBULL_PORT := 8000
endif

ifndef COWBULL_SERVER
  override COWBULL_SERVER := localhost
endif

ifndef COWBULL_SERVER_IMAGE
  override COWBULL_SERVER_IMAGE := dsanderscan/cowbull:20.03-2
endif

ifndef HOMEDIR
  override HOMEDIR := $(shell echo ~)
endif

ifndef HOST_IF
  override HOST_IF := en5
endif

ifndef HOST_IP
  override HOST_IP := $(shell ipconfig getifaddr $(HOST_IF))
endif

ifndef IMAGE_NAME
  override IMAGE_NAME := cowbull_webapp
endif

ifndef IMAGE_REG
  override IMAGE_REG := dsanderscan
endif

ifndef MAJOR
  override MAJOR := 20
endif

ifndef MINOR
  override MINOR := 03
endif

ifndef REDIS_PORT
  override REDIS_PORT := 6379
endif

ifndef VENV
	override VENV := $(HOMEDIR)/virtuals/cowbull_webapp_p3/bin/activate
endif

ifndef WORKDIR
  override WORKDIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
endif

define start_docker
	docker run \
	  --detach \
	  --name redis \
	  -p $(REDIS_PORT):6379 \
	  redis:alpine3.11; \
	docker run \
	  --name cowbull_server \
	  -p $(COWBULL_PORT):8080 \
	  --env PORT=8080 \
	  --env LOGGING_LEVEL=$(1) \
	  --env PERSISTER='{"engine_name": "redis", "parameters": {"host": "$(HOST_IP)", "port": 6379, "db": 0}}' \
	  --detach \
	  $(COWBULL_SERVER_IMAGE)
endef

define stop_docker
	echo; \
	echo "Stopping Docker cowbull container "; \
	docker stop cowbull_server; \
	echo "Removing Docker cowbull container"; \
	docker rm cowbull_server; \
	echo "Stopping Docker Redis container "; \
	docker stop redis; \
	echo "Removing Docker Redis container"; \
	docker rm redis; \
	echo; \
	echo
endef

define end_log
	echo; \
	echo "Started $(1) at  : $(2)"; \
	echo "Finished $(1) at : $(3)"; \
	echo
endef

.PHONY: build debug push run shell test

build:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	docker build \
		-t $(IMAGE_REG)/$(IMAGE_NAME):$(MAJOR).$(MINOR)-$(BUILD_NUMBER) \
		. ; \
	$(call end_log,"build",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))

debug:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	source $(VENV); \
	$(call start_docker,10); \
	PYTHONPATH=$(WORKDIR) \
		LOGGING_LEVEL=10 \
		COWBULL_PORT=$(COWBULL_PORT) \
		COWBULL_SERVER=$(COWBULL_SERVER) \
		python app.py; \
	deactivate; \
	$(call stop_docker); \
	$(call end_log,"debug",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))

push:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	docker push $(IMAGE_REG)/$(IMAGE_NAME):$(MAJOR).$(MINOR)-$(BUILD_NUMBER); \
	$(call end_log,"push",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))

run:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	source $(VENV); \
	$(call start_docker,30); \
	PYTHONPATH=$(WORKDIR) \
		LOGGING_LEVEL=30 \
		COWBULL_PORT=$(COWBULL_PORT) \
		COWBULL_SERVER=$(COWBULL_SERVER) \
		python app.py; \
	deactivate; \
	$(call stop_docker);  \
	$(call end_log,"run",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))

shell:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	docker run \
		-it --rm  \
		$(IMAGE_REG)/$(IMAGE_NAME):$(MAJOR).$(MINOR)-$(BUILD_NUMBER) /bin/sh; \
	$(call end_log,"run",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))

test:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	source $(VENV); \
	PYTHONPATH=$(WORKDIR) \
		LOGGING_LEVEL=30 \
		python tests/main.py; \
	deactivate; \
	$(call end_log,"tests",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))
