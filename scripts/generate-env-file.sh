#!/bin/bash
VPS_USERNAME="$1"
VPS_HOST="$2"
SSH_PRIVATE_KEY="$3"
JWT_KEY="$4"

VPS_USERNAME_HOST=${VPS_USERNAME}@${VPS_HOST}

ENV_FILE=".env" 

ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"JWT_KEY=$JWT_KEY\" > \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"GOOGLE_KEY=$GOOGLE_KEY\" >> \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"DB_PASSWORD=$DB_PASSWORD\" >> \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"DB_USER=$DB_USER\" >> \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"DB_URL=$DB_URL\" >> \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"DB_DATATABLE=$DB_DATATABLE\" >> \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"EMAIL_SERVER=$EMAIL_SERVER\" >> \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"EMAIL_USER=$EMAIL_USER\" >> \"$ENV_FILE\""
ssh ${VPS_USERNAME_HOST} "cd SemanaTeste && echo \"EMAIL_PASSWORD=$EMAIL_PASSWORD\" >> \"$ENV_FILE\""