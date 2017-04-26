#!/bin/bash         

label=`python generate_aniso_networks_label.py` ;

smt run --executable=/home/docker/env/neurosci/bin/python --main=generate_aniso_networks.py --reason='generate aniso networks' --label=$label --tag=aniso,netw params/generate_aniso_networks_params.py


