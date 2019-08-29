FROM	alpine:3.10.2
RUN		apk update \
		&& addgroup -g 10000 cowbull_wa \
		&& mkdir /cowbull \
		&& adduser -u 10000 -G cowbull_wa --disabled-password --home /cowbull cowbull \
		&& chown cowbull /cowbull \
		&& apk add --update \
			curl \
			musl \
			python3 \
			py3-pip \
		&& curl -Lo /tmp/curl-7.65.3-r0.apk http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/curl-7.65.3-r0.apk \
		&& apk add /tmp/curl-7.65.3-r0.apk \
		&& curl -Lo /tmp/musl-1.1.23-r3.apk http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/musl-1.1.23-r3.apk \
		&& apk add /tmp/musl-1.1.23-r3.apk \
		&& curl -Lo /tmp/musl-utils-1.1.23-r3.apk http://dl-3.alpinelinux.org/alpine/edge/main/x86_64/musl-utils-1.1.23-r3.apk \
		&& apk add /tmp/musl-utils-1.1.23-r3.apk
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
	CMD [ "/bin/bash", "-c", "/cowbull/healthcheck/healthcheck.sh" ]

CMD		["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]
EXPOSE	8080
LABEL	MAINTAINER="dsanderscanada@gmail.com"