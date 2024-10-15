#!/bin/bash

# docker run -it --rm -p "8000:8000" frankjoshua/excel_bot:latest $@
docker run -it --rm -v "$PWD:/home/jovyan/work/" --network="host" frankjoshua/excel_bot $@