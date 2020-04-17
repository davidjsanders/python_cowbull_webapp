# FROM	alpine:3.11
FROM	python:3.8.2-slim-buster
RUN		DEBIAN_FRONTEND=noninteractive apt-get update \
		&& DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes \
		&& DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade --yes
RUN		DEBIAN_FRONTEND=noninteractive addgroup --gid 10000 cowbull_wa \
		&& DEBIAN_FRONTEND=noninteractive adduser \
			--uid 10000 \
			--ingroup cowbull_wa \
			--disabled-password \
			--home /cowbull \
			--gecos "" \
			cowbull \
		&& chown cowbull /cowbull
WORKDIR	/cowbull
COPY	requirements.txt /cowbull/
RUN		pip3 install --upgrade pip \
		&& pip3 install -r /cowbull/requirements.txt

USER	cowbull
ENV		PYTHONPATH="/cowbull:/cowbull/tests"
COPY 	. ./

USER 	root
RUN 	chmod +x \
			/cowbull/healthcheck/healthcheck.sh \
			/cowbull/healthcheck/liveness.sh \
			/cowbull/entrypoint.sh

USER	cowbull
ARG     build_number=latest
ENV     BUILD_NUMBER=${build_number}
ENV     COWBULL_ENVIRONMENT=20.04-28
HEALTHCHECK \
	--interval=10s \
	--timeout=5s \
	--start-period=10s \
	--retries=3 \
	CMD [ "/bin/sh", "-c", "/cowbull/healthcheck/healthcheck.sh" ]

ENTRYPOINT [ "/cowbull/entrypoint.sh" ]
#CMD		["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]
EXPOSE	8080
LABEL	MAINTAINER="dsanderscanada@gmail.com"
LABEL 	BUILD="${BUILD_NUMBER}"