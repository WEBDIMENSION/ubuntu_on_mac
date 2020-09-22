#!/usr/bin/env bash
docker rm -f dev
docker rmi  dev
docker rm -f act-develop-build
act push
