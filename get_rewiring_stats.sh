#!/bin/bash         

name='get_rewiring_stats';
label=`python comp/get_rewiring_stats_label.py` ;

g1='data/aniso-netw_N1000_w37.3_ed-l296_4GX7-9f2f.gt';
g2='data/aniso-netw_N1000_w37.3_ed-l296_4GX7-2809.gt';
g3='data/aniso-netw_N1000_w37.3_ed-l296_4GX7-bc48.gt';
g4='data/aniso-netw_N1000_w37.3_ed-l296_4GX7-e6d8.gt';
g5='data/aniso-netw_N1000_w37.3_ed-l296_4GX7-ea07.gt';

python comp/$name.py $g1 $g2 $g3 comp/params/$name\_params.py

# smt run --executable=/home/docker/env/neurosci/bin/python --main=comp/$name.py --reason='get rewiring stats' --label=$label --tag=aniso,netw $g1 $g2 $g3 comp/params/$name\_params.py

# cp comp/params/$name\_params.py data/$label\_params.py
# cp $BASH_SOURCE data/$label"_run.sh"
