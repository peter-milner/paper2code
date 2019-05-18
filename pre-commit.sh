#!/bin/bash -xe

docker exec my-p2p /bin/sh -c "cd .. && pipenv run pylint app/*.py"

if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi