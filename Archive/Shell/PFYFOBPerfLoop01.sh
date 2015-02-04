#!/usr/bin/env bash

SIM_FILE_NAME=$1
INI_PROFILE_NAME=$2
INI_FILE_NAME=$3
ITERATION_COUNT=$4

timestamp() 
{
  date +%Y%m%d%H%M
}
timestamp
echo $ITERATION_COUNT
for ((i=1;i<=$ITERATION_COUNT;i++));
do
#	negative_x_displacement=$(shuf -i 5-250 -n 1)
#	positive_x_displacement=$(shuf -i 5-260 -n 1)
#	fob_length=$(shuf -i 120-400 -n 1)
#	fob_count=$(shuf -i 3-10 -n 1)
	#echo $positive_x_displacement
	#python3 SimplifiedYardSim17.py $negative_x_displacement $positive_x_displacement $fob_length &
	#python3 PFYFOBPerf01.py $negative_x_displacement $positive_x_displacement $fob_length $fob_count &

	python3 $SIM_FILE_NAME $INI_FILE_NAME $INI_PROFILE_NAME &
	wait
done
