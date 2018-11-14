#!/usr/bin/env bash
docker-machine create \
   --driver virtualbox \
   --virtualbox-boot2docker-url=https://github.com/boot2docker/boot2docker/releases/download/v18.06.1-ce/boot2docker.iso \
   --engine-opt experimental=true \
   --engine-opt metrics-addr=0.0.0.0:9323 \
   --virtualbox-memory=2048 \
   mgr
docker-machine create \
   --driver virtualbox \
   --virtualbox-boot2docker-url=https://github.com/boot2docker/boot2docker/releases/download/v18.06.1-ce/boot2docker.iso \
   --engine-opt experimental=true \
   --engine-opt metrics-addr=0.0.0.0:9323 \
   --virtualbox-memory=2048 \
   --virtualbox-cpu-count=2 \
   worker-1
docker-machine create \
   --driver virtualbox \
   --virtualbox-boot2docker-url=https://github.com/boot2docker/boot2docker/releases/download/v18.06.1-ce/boot2docker.iso \
   --engine-opt experimental=true \
   --engine-opt metrics-addr=0.0.0.0:9323 \
   --virtualbox-memory=2048 \
   --virtualbox-cpu-count=2 \
   worker-2
docker-machine ssh mgr docker swarm init --advertise-addr=$(docker-machine ip mgr)
jointoken=$(docker-machine ssh mgr docker swarm join-token worker -q)
docker-machine ssh worker-1 docker swarm join --token ${jointoken} $(docker-machine ip mgr):2377
docker-machine ssh worker-2 docker swarm join --token ${jointoken} $(docker-machine ip mgr):2377
