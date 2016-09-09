#!/bin/bash

docker run -it -p 127.0.0.1:8015:8000 \
       --user="$(id -u):$(id -g)" \
       -v $(pwd):/home/lab \
       felix11h/aniso_netw_env \
       /bin/bash -c \
       'source /home/docker/env/neurosci/bin/activate;
        screen -d -m /home/docker/env/neurosci/bin/smtweb --allips;
        source startup_messg.sh;
        bash'
