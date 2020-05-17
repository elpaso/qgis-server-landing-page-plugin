#!/bin/bash
docker run -it -p8000:8000 -p8080:8080 -w `pwd` -v /home/${USER}:/home/${USER} -v `pwd`:`pwd` --user 1000  --rm elpaso/vue-builder:latest $@



