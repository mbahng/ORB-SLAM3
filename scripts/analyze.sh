#!/bin/bash

cd .. 

datasets=("av512m" "av512s" "euroc_mh1_752" "euroc_mh2_752" "euroc_mh3_752" "euroc_mh4_752" "euroc_mh5_752" "euroc_v101_752" "euroc_v102_752" "euroc_v103_752" "euroc_v201_752" "euroc_v202_752" "euroc_v203_752" "tum_room1_512" "tum_room2_512" "tum_room3_512" "tum_room4_512" "tum_room5_512" "tum_room6_512")

for dataset in ${datasets[@]}
do 
  for threshold in 500 750 1000 1250 2500 5000 10000 
  do 
    for seed in 1 2 3 
    do 
      python results/analyze.py --dataset ${dataset} --threshold ${threshold} --seed ${seed} --keypoints_vs_tracking
    done 
  done
done 


