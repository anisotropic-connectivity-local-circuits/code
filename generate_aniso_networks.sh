#!/bin/bash         

name='generate_aniso_networks';
label=`python comp/generate_aniso_networks_label.py` ;

smt run --executable=/home/docker/env/neurosci/bin/python --main=comp/$name.py --reason='generate aniso networks' --label=$label --tag=aniso,netw comp/params/$name\_params.py

cp comp/params/$name\_params.py data/$label\_params.py
cp $BASH_SOURCE data/$label"_run.sh"
