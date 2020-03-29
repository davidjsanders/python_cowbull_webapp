ifndef WORKDIR
  override WORKDIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
endif

ifndef HOMEDIR
  override HOMEDIR := $(shell echo ~)
endif

ifndef VENV
	override VENV := $(HOMEDIR)/virtuals/cowbull_webapp_p3/bin/activate
endif

ifndef HOST_IP
  override HOST_IP := $(shell ipconfig getifaddr en5)
endif

ifndef COWBULL_SERVER_IMAGE
  override COWBULL_SERVER_IMAGE := dsanderscan/cowbull:20.03-2
endif

ifndef COWBULL_SERVER
  override COWBULL_SERVER := localhost
endif

ifndef COWBULL_PORT
  override COWBULL_PORT := 8000
endif

define stop_docker
	echo; \
	echo "Stopping Docker container "; \
	docker stop cowbull_server; \
	echo "Removing Docker container"; \
	docker rm cowbull_server; \
	echo
endef

define end_log
	echo; \
	echo "Started $(1) at  : $(2)"; \
	echo "Finished $(1) at : $(3)"; \
	echo
endef

.PHONY: debug run test

test:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	source $(VENV); \
	PYTHONPATH=$(WORKDIR) \
		LOGGING_LEVEL=30 \
		python tests/main.py; \
	deactivate; \
	$(call end_log,"tests",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))

debug:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	source $(VENV); \
	docker run \
	  --name cowbull_server \
	  -p $(COWBULL_PORT):8080 \
	  --env PORT=8080 \
	  --env LOGGING_LEVEL=10 \
	  --env PERSISTER='{"engine_name": "redis", "parameters": {"host": "$(HOST_IP)", "port": 6379, "db": 0}}' \
	  --detach \
	  $(COWBULL_SERVER_IMAGE); \
	PYTHONPATH=$(WORKDIR) \
		LOGGING_LEVEL=10 \
		COWBULL_PORT=$(COWBULL_PORT) \
		COWBULL_SERVER=$(COWBULL_SERVER) \
		python app.py; \
	deactivate; \
	$(call stop_docker) \
	$(call end_log,"debug",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))

run:
	@start="`date +"%d%m%YT%H:%M:%S%Z"`"; \
	source $(VENV); \
	docker run \
	  --name cowbull_server \
	  -p $(COWBULL_PORT):8080 \
	  --env PORT=8080 \
	  --env LOGGING_LEVEL=30 \
	  --env PERSISTER='{"engine_name": "redis", "parameters": {"host": "$(HOST_IP)", "port": 6379, "db": 0}}' \
	  --detach \
	  $(COWBULL_SERVER_IMAGE); \
	PYTHONPATH=$(WORKDIR) \
		LOGGING_LEVEL=30 \
		COWBULL_PORT=$(COWBULL_PORT) \
		COWBULL_SERVER=$(COWBULL_SERVER) \
		python app.py; \
	deactivate; \
	$(call stop_docker);  \
	$(call end_log,"run",$$start,$(shell date +"%d%m%YT%H:%M:%S%Z"))
