#!/bin/bash -xe

docker exec my-p2p /bin/sh -c "pipenv run pylint app"

if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi