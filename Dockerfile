FROM	alpine:3.10.2
ARG		curl_url=curl-7.69.1-r0.apk
ARG     musl_url=musl-1.1.24-r4.apk 
ARG 	musl_util_url=musl-1.1.24-r4.apk
RUN		apk update \
		&& addgroup -g 10000 cowbull_wa \
		&& mkdir /cowbull \
		&& adduser -u 10000 -G cowbull_wa --disabled-password --home /cowbull cowbull \
		&& chown cowbull /cowbull \
		&& apk add --update \
			curl \
			musl \
			python3 \
			py3-pip
RUN		curl -Lo /tmp/${curl_url} http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/${curl_url} \
		&& apk add /tmp/${curl_url} \
		&& curl -Lo /tmp/${musl_url} http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/${musl_url} \
		&& apk add /tmp/${musl_url} \
		&& curl -Lo /tmp/${musl_util_url} http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/${musl_util_url} \
		&& apk add /tmp/${musl_util_url}
WORKDIR	/cowbull
COPY	requirements.txt /cowbull/
RUN		pip3 install --upgrade pip \
		&& pip3 install -r /cowbull/requirements.txt
USER	cowbull
ENV		PYTHONPATH="/cowbull:/cowbull/tests"
COPY	GameSPA /cowbull/GameSPA/
COPY    Health /cowbull/Health/
COPY	templates /cowbull/templates/
COPY	initialization_package /cowbull/initialization_package/
COPY	static /cowbull/static/
COPY 	tests /cowbull/tests/
COPY 	healthcheck /cowbull/healthcheck/

COPY    app.py  /cowbull/
COPY	__init__.py /cowbull/
COPY    LICENSE /cowbull/

USER 	root
RUN 	chmod +x \
			/cowbull/healthcheck/healthcheck.sh \
			/cowbull/healthcheck/liveness.sh

USER	cowbull
HEALTHCHECK \
	--interval=10s \
	--timeout=5s \
	--start-period=10s \
	--retries=3 \
	CMD [ "/bin/sh", "-c", "/cowbull/healthcheck/healthcheck.sh" ]

CMD		["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]
EXPOSE	8080
LABEL	MAINTAINER="dsanderscanada@gmail.com"