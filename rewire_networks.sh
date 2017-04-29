#!/bin/bash         

name='rewire_networks';
#label=`python comp/generate_aniso_networks_label.py` ;

g1='/home/lab/data/aniso-netw_N1000_w37.3_ed-l296_4GX7-9f2f.gt';
g2='/home/lab/data/aniso-netw_N1000_w37.3_ed-l296_4GX7-2809.gt';
g3='/home/lab/data/aniso-netw_N1000_w37.3_ed-l296_4GX7-bc48.gt';
g4='/home/lab/data/aniso-netw_N1000_w37.3_ed-l296_4GX7-e6d8.gt';
g5='/home/lab/data/aniso-netw_N1000_w37.3_ed-l296_4GX7-ea07.gt';

#python comp/$name.py $g1 $g2 $g3 $g4 $g5 comp/params/$name\_params.py
python comp/$name.py /home/lab/data/N1000_w126_manual.gt comp/params/$name\_params.py

# smt run --executable=/home/docker/env/neurosci/bin/python --main=comp/$name.py --reason='rewire aniso networks' --label=$label --tag=aniso,netw comp/params/$name\_params.py

# cp comp/params/$name\_params.py data/$label\_params.py
# cp $BASH_SOURCE data/$label"_run.sh"
