#!/bin/bash

if [[ -z $1 ]]; then
echo "Please provide host, example ubuntu@158.101.126.224"
exit 1
fi

# Read the environmental variable from .env file
if [[ -f .env ]]; then
  source .env
else
  echo ".env file not found"
  exit 1
fi

echo "$1" > tmp_inventory
echo "[chat_bot]" >> tmp_inventory
echo "$1" >> tmp_inventory

ansible-playbook -i tmp_inventory --extra-vars "OPENAI_API_KEY=$OPENAI_API_KEY" ansible/all.yml

rm tmp_inventory