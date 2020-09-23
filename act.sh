#!/usr/bin/env bash

docker rm -f ubuntu18.04
docker rmi  ubuntu18.04
docker rm -f ubuntu20.04
docker rmi  ubuntu20.04
docker rm -f act-tests-build
act push
