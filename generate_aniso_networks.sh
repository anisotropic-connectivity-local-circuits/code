#!/bin/bash         

name='generate_aniso_networks';
label=`python generate_aniso_networks_label.py` ;

smt run --executable=/home/docker/env/neurosci/bin/python --main=comp/$name.py --reason='generate aniso networks' --label=$label --tag=aniso,netw params/$name\_params.py

cp params/$name\_params.py data/$label\_params.py
cp $BASH_SOURCE data/$label"_run.sh"
