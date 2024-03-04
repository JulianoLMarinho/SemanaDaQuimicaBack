#!/bin/bash

VPS_USERNAME="$1"
VPS_HOST="$2"
SSH_PRIVATE_KEY="$3"

VPS_USERNAME_HOST=${VPS_USERNAME}@${VPS_HOST}

eval $(ssh-agent -s)

ssh-add <(echo "$SSH_PRIVATE_KEY")

ssh ${VPS_USERNAME_HOST} "rm -rf SemanaDaQuimica"

ssh ${VPS_USERNAME_HOST} "mkdir SemanaDaQuimica"

scp -r app ${VPS_USERNAME_HOST}:~/SemanaDaQuimica
scp requirements.txt ${VPS_USERNAME_HOST}:~/SemanaDaQuimica
scp .env ${VPS_USERNAME_HOST}:~/SemanaDaQuimica

ssh ${VPS_USERNAME_HOST} "cd SemanaDaQuimica && python3 -m virtualenv venv"
ssh ${VPS_USERNAME_HOST} "cd SemanaDaQuimica && source venv/bin/activate && pip install -r requirements.txt"

ssh ${VPS_USERNAME_HOST} "sudo systemctl restart fastapi.service"
