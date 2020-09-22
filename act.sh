#!/usr/bin/env bash

docker rm -f dev
docker rmi  dev
docker rm -f act-tests-build
act push
