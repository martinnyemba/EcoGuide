#!/usr/bin/env bash

# Load environment variables from .env file
# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs)

# Set each environment variable on Heroku
while IFS= read -r line; do
    if [[ ! $line =~ ^# && $line =~ = ]]; then
        varname=$(echo "$line" | cut -d '=' -f 1)
        varvalue=$(echo "$line" | cut -d '=' -f 2-)
        heroku config:set "$varname=$varvalue"
    fi
done < .env
