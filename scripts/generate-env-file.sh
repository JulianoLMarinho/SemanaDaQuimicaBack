#!/bin/bash

ENV_FILE=".env" 

echo "JWT_KEY=$JWT_KEY" > "$ENV_FILE"
echo "GOOGLE_KEY=$GOOGLE_KEY" >> "$ENV_FILE"
echo "DB_PASSWORD=$DB_PASSWORD" >> "$ENV_FILE"
echo "DB_USER=$DB_USER" >> "$ENV_FILE"
echo "DB_URL=$DB_URL" >> "$ENV_FILE"
echo "DB_DATATABLE=$DB_DATATABLE" >> "$ENV_FILE"
echo "EMAIL_SERVER=$EMAIL_SERVER" >> "$ENV_FILE"
echo "EMAIL_USER=$EMAIL_USER" >> "$ENV_FILE"
echo "EMAIL_PASSWORD=$EMAIL_PASSWORD" >> "$ENV_FILE"