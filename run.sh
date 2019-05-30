#!/bin/bash

a=(350 400)
# ratio=(1 0.95 0.85 0.8)
ratio=(1)
topo=('Abilene' 'AttMpls')

for var_a in ${a[@]};
do
	for var_r in ${ratio[@]};
	do
		for var_t in ${topo[@]};
		do
		    python ./main.py -a ${var_a} -r ${var_r} --topo=${var_t}
			# python ./main.py -a ${var_a} -r ${var_r} --topo=${var_t} 2>&1 >> data/output/output${var_t}_${var_a}_${var_r}
		done
	done
done
