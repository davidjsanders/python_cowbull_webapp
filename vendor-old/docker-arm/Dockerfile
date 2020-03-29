FROM		arm32v5/python:3.5.3-slim
MAINTAINER	David Sanders
RUN		apt-get update && \
		groupadd -r cowbull_wa && \
		mkdir /cowbull && \
		useradd -r -G cowbull_wa -d /cowbull cowbull && \
		chown cowbull /cowbull
WORKDIR		/cowbull
COPY		requirements.txt /cowbull/
RUN		pip install -q -r /cowbull/requirements.txt
USER		cowbull
ENV		PYTHONPATH="/cowbull"
COPY		GameSPA /cowbull/GameSPA/
COPY		templates /cowbull/templates/
COPY		initialization_package /cowbull/initialization_package/
COPY		static /cowbull/static/

COPY        	app.py  /cowbull/
COPY		__init__.py /cowbull/
COPY        	LICENSE /cowbull/
CMD		["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]
EXPOSE		8080
