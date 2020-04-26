# FROM	alpine:3.11
FROM	python:3.6.10-alpine3.11
ARG		curl_url=curl-7.69.1-r0.apk
ARG     musl_url=musl-1.1.24-r6.apk 
ARG 	musl_util_url=musl-utils-1.1.24-r6.apk
RUN		apk update
RUN		apk add --update \
			curl \
			musl \
			# python3 \
			# py3-pip \
		&& curl -Lo /tmp/${curl_url} http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/${curl_url} \
		&& apk add /tmp/${curl_url} \
		&& curl -Lo /tmp/${musl_url} http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/${musl_url} \
		&& apk add /tmp/${musl_url} \
		&& curl -Lo /tmp/${musl_util_url} http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/${musl_util_url} \
		&& apk add /tmp/${musl_util_url}
RUN		addgroup -g 10000 cowbull_wa \
		&& mkdir /cowbull \
		&& adduser -u 10000 -G cowbull_wa --disabled-password --home /cowbull cowbull \
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
			/cowbull/entrypoint.sh \
&&      chown -R cowbull:cowbull_wa /cowbull

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
