#!/bin/bash

docker run -it --rm -p "8000:8000" frankjoshua/archreactor_bot:latest $@
#docker run -it --rm -v "$PWD:/home/jovyan/work/" -p "8000:8000" frankjoshua/archreactor_bot $@