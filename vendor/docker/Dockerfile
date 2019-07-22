FROM		python:3.5.3-slim
MAINTAINER	David Sanders
RUN		apt-get update && \
		apt-get install --yes curl && \
		groupadd -r cowbull_wa && \
		mkdir /cowbull && \
		useradd -r -G cowbull_wa -d /cowbull cowbull && \
		chown cowbull /cowbull
WORKDIR	/cowbull
COPY	requirements.txt /cowbull/
RUN		pip install -q -r /cowbull/requirements.txt
USER	cowbull
ENV		PYTHONPATH="/cowbull:/cowbull/tests"
COPY	GameSPA /cowbull/GameSPA/
COPY    Health /cowbull/Health/
COPY	templates /cowbull/templates/
COPY	initialization_package /cowbull/initialization_package/
COPY	static /cowbull/static/
COPY 	tests /cowbull/tests/
COPY 	healthcheck /cowbull/healthcheck/

COPY        	app.py  /cowbull/
COPY		__init__.py /cowbull/
COPY        	LICENSE /cowbull/

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
EXPOSE		8080
LABEL MAINTAINER="dsanderscanada@gmail.com"