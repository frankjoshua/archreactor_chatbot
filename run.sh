#!/bin/bash

cd server
uvicorn server:app --reload