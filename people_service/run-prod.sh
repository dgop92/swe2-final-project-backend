#!/bin/sh

if [ "$1" = "create" ]; then
    uvicorn services.create_service:app --host "0.0.0.0" --port 8011
elif [ "$1" = "read" ]; then
    uvicorn services.read_service:app --host "0.0.0.0" --port 8012
elif [ "$1" = "update" ]; then
    uvicorn services.update_service:app --host "0.0.0.0" --port 8013
elif [ "$1" = "delete" ]; then
    uvicorn services.delete_service:app --host "0.0.0.0" --port 8014
else
    echo "Invalid parameter. Usage: ./script.sh [create|read|update|delete]"
fi