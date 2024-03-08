#!/bin/bash

cd .. 

for seed in 1 2 3
do 
  for threshold in 500 750 1000 1250 2500 5000 10000
  do 
    echo "Starting Seed Threshold : " $seed $threshold

    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/dataset-room1_512_16/$threshold.yaml data/dataset-room1_512_16/mav0/cam0/data Examples/Monocular/TUM_TimeStamps/dataset-room1_512.txt tum_rm1_512_t${threshold}_s$seed &&
    # mkdir -p results/tum_room1_512/$threshold/seed$seed && 
    # mv f_tum_rm1_512_t${threshold}_s${seed}.txt results/tum_room1_512/$threshold/seed$seed &&
    # mv kf_tum_rm1_512_t${threshold}_s${seed}.txt results/tum_room1_512/$threshold/seed$seed &&
    # mv keypoints.txt results/tum_room1_512/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/dataset-room2_512_16/$threshold.yaml data/dataset-room2_512_16/mav0/cam0/data Examples/Monocular/TUM_TimeStamps/dataset-room2_512.txt tum_rm2_512_t${threshold}_s$seed &&
    # mkdir -p results/tum_room2_512/$threshold/seed$seed && 
    # mv f_tum_rm2_512_t${threshold}_s${seed}.txt results/tum_room2_512/$threshold/seed$seed &&
    # mv kf_tum_rm2_512_t${threshold}_s${seed}.txt results/tum_room2_512/$threshold/seed$seed &&
    # mv keypoints.txt results/tum_room2_512/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/dataset-room3_512_16/$threshold.yaml data/dataset-room3_512_16/mav0/cam0/data Examples/Monocular/TUM_TimeStamps/dataset-room3_512.txt tum_rm3_512_t${threshold}_s$seed &&
    # mkdir -p results/tum_room3_512/$threshold/seed$seed && 
    # mv f_tum_rm3_512_t${threshold}_s${seed}.txt results/tum_room3_512/$threshold/seed$seed &&
    # mv kf_tum_rm3_512_t${threshold}_s${seed}.txt results/tum_room3_512/$threshold/seed$seed &&
    # mv keypoints.txt results/tum_room3_512/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/dataset-room4_512_16/$threshold.yaml data/dataset-room4_512_16/mav0/cam0/data Examples/Monocular/TUM_TimeStamps/dataset-room4_512.txt tum_rm4_512_t${threshold}_s$seed &&
    # mkdir -p results/tum_room4_512/$threshold/seed$seed && 
    # mv f_tum_rm4_512_t${threshold}_s${seed}.txt results/tum_room4_512/$threshold/seed$seed &&
    # mv kf_tum_rm4_512_t${threshold}_s${seed}.txt results/tum_room4_512/$threshold/seed$seed &&
    # mv keypoints.txt results/tum_room4_512/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/dataset-room5_512_16/$threshold.yaml data/dataset-room5_512_16/mav0/cam0/data Examples/Monocular/TUM_TimeStamps/dataset-room5_512.txt tum_rm5_512_t${threshold}_s$seed &&
    # mkdir -p results/tum_room5_512/$threshold/seed$seed && 
    # mv f_tum_rm5_512_t${threshold}_s${seed}.txt results/tum_room5_512/$threshold/seed$seed &&
    # mv kf_tum_rm5_512_t${threshold}_s${seed}.txt results/tum_room5_512/$threshold/seed$seed &&
    # mv keypoints.txt results/tum_room5_512/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/dataset-room6_512_16/$threshold.yaml data/dataset-room6_512_16/mav0/cam0/data Examples/Monocular/TUM_TimeStamps/dataset-room6_512.txt tum_rm6_512_t${threshold}_s$seed &&
    # mkdir -p results/tum_room6_512/$threshold/seed$seed && 
    # mv f_tum_rm6_512_t${threshold}_s${seed}.txt results/tum_room6_512/$threshold/seed$seed &&
    # mv kf_tum_rm6_512_t${threshold}_s${seed}.txt results/tum_room6_512/$threshold/seed$seed &&
    # mv keypoints.txt results/tum_room6_512/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/MH_01_easy/$threshold.yaml data/MH_01_easy/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/MH01.txt euroc_mh1_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_mh1_752/$threshold/seed$seed && 
    # mv f_euroc_mh1_752t${threshold}_s${seed}.txt results/euroc_mh1_752/$threshold/seed$seed &&
    # mv kf_euroc_mh1_752t${threshold}_s${seed}.txt results/euroc_mh1_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_mh1_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/MH_02_easy/$threshold.yaml data/MH_02_easy/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/MH02.txt euroc_mh2_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_mh2_752/$threshold/seed$seed && 
    # mv f_euroc_mh2_752t${threshold}_s${seed}.txt results/euroc_mh2_752/$threshold/seed$seed &&
    # mv kf_euroc_mh2_752t${threshold}_s${seed}.txt results/euroc_mh2_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_mh2_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/MH_03_medium/$threshold.yaml data/MH_03_medium/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/MH03.txt euroc_mh3_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_mh3_752/$threshold/seed$seed && 
    # mv f_euroc_mh3_752t${threshold}_s${seed}.txt results/euroc_mh3_752/$threshold/seed$seed &&
    # mv kf_euroc_mh3_752t${threshold}_s${seed}.txt results/euroc_mh3_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_mh3_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/MH_04_difficult/$threshold.yaml data/MH_04_difficult/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/MH04.txt euroc_mh4_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_mh4_752/$threshold/seed$seed && 
    # mv f_euroc_mh4_752t${threshold}_s${seed}.txt results/euroc_mh4_752/$threshold/seed$seed &&
    # mv kf_euroc_mh4_752t${threshold}_s${seed}.txt results/euroc_mh4_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_mh4_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/MH_05_difficult/$threshold.yaml data/MH_05_difficult/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/MH05.txt euroc_mh5_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_mh5_752/$threshold/seed$seed && 
    # mv f_euroc_mh5_752t${threshold}_s${seed}.txt results/euroc_mh5_752/$threshold/seed$seed &&
    # mv kf_euroc_mh5_752t${threshold}_s${seed}.txt results/euroc_mh5_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_mh5_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/V1_01_easy/$threshold.yaml data/V1_01_easy/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/V101.txt euroc_v101_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_v101_752/$threshold/seed$seed && 
    # mv f_euroc_v101_752t${threshold}_s${seed}.txt results/euroc_v101_752/$threshold/seed$seed &&
    # mv kf_euroc_v101_752t${threshold}_s${seed}.txt results/euroc_v101_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_v101_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/V1_02_medium/$threshold.yaml data/V1_02_medium/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/V102.txt euroc_v102_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_v102_752/$threshold/seed$seed && 
    # mv f_euroc_v102_752t${threshold}_s${seed}.txt results/euroc_v102_752/$threshold/seed$seed &&
    # mv kf_euroc_v102_752t${threshold}_s${seed}.txt results/euroc_v102_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_v102_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/V1_03_difficult/$threshold.yaml data/V1_03_difficult/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/V103.txt euroc_v103_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_v103_752/$threshold/seed$seed && 
    # mv f_euroc_v103_752t${threshold}_s${seed}.txt results/euroc_v103_752/$threshold/seed$seed &&
    # mv kf_euroc_v103_752t${threshold}_s${seed}.txt results/euroc_v103_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_v103_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/V2_01_easy/$threshold.yaml data/V2_01_easy/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/V201.txt euroc_v201_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_v201_752/$threshold/seed$seed && 
    # mv f_euroc_v201_752t${threshold}_s${seed}.txt results/euroc_v201_752/$threshold/seed$seed &&
    # mv kf_euroc_v201_752t${threshold}_s${seed}.txt results/euroc_v201_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_v201_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/V2_02_medium/$threshold.yaml data/V2_02_medium/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/V202.txt euroc_v202_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_v202_752/$threshold/seed$seed && 
    # mv f_euroc_v202_752t${threshold}_s${seed}.txt results/euroc_v202_752/$threshold/seed$seed &&
    # mv kf_euroc_v202_752t${threshold}_s${seed}.txt results/euroc_v202_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_v202_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/V2_03_difficult/$threshold.yaml data/V2_03_difficult/mav0/cam0/data Examples/Monocular/EuRoC_TimeStamps/V203.txt euroc_v203_752t${threshold}_s$seed &&
    # mkdir -p results/euroc_v203_752/$threshold/seed$seed && 
    # mv f_euroc_v203_752t${threshold}_s${seed}.txt results/euroc_v203_752/$threshold/seed$seed &&
    # mv kf_euroc_v203_752t${threshold}_s${seed}.txt results/euroc_v203_752/$threshold/seed$seed &&
    # mv keypoints.txt results/euroc_v203_752/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/256x144_moving/$threshold.yaml data/256x144_moving/data data/256x144_moving/timestamps.txt av256m_t${threshold}_s$seed &&
    # mkdir -p results/av256m/$threshold/seed$seed &&
    # mv f_av256m_t${threshold}_s${seed}.txt results/av256m/$threshold/seed$seed && 
    # mv kf_av256m_t${threshold}_s${seed}.txt results/av256m/$threshold/seed$seed && 
    # mv keypoints.txt results/av256m/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/256x144_stationary/$threshold.yaml data/256x144_stationary/data data/256x144_stationary/timestamps.txt av256s_t${threshold}_s$seed && 
    # mkdir -p results/av256s/$threshold/seed$seed &&
    # mv f_av256s_t${threshold}_s${seed}.txt results/av256s/$threshold/seed$seed && 
    # mv kf_av256s_t${threshold}_s${seed}.txt results/av256s/$threshold/seed$seed && 
    # mv keypoints.txt results/av256s/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/512x288_moving/$threshold.yaml data/512x288_moving/data data/512x288_moving/timestamps.txt av512m_t${threshold}_s$seed && 
    # mkdir -p results/av512m/$threshold/seed$seed && 
    # mv f_av512m_t${threshold}_s${seed}.txt results/av512m/$threshold/seed$seed &&
    # mv kf_av512m_t${threshold}_s${seed}.txt results/av512m/$threshold/seed$seed &&
    # mv keypoints.txt results/av512m/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/512x288_stationary/$threshold.yaml data/512x288_stationary/data data/512x288_stationary/timestamps.txt av512s_t${threshold}_s$seed && 
    # mkdir -p results/av512s/$threshold/seed$seed &&
    # mv f_av512s_t${threshold}_s${seed}.txt results/av512s/$threshold/seed$seed &&
    # mv kf_av512s_t${threshold}_s${seed}.txt results/av512s/$threshold/seed$seed &&
    # mv keypoints.txt results/av512s/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/960x720_KilgoB1/$threshold.yaml data/960x720_KilgoB1/data data/960x720_KilgoB1/timestamps.txt kb960_t${threshold}_s$seed && 
    # mkdir -p results/kb960/$threshold/seed$seed && 
    # mv f_kb960_t${threshold}_s${seed}.txt results/kb960/$threshold/seed$seed && 
    # mv kf_kb960_t${threshold}_s${seed}.txt results/kb960/$threshold/seed$seed && 
    # mv keypoints.txt results/kb960/$threshold/seed$seed 
    # rm keypoints.txt
    # rm f_*
    # rm kf_*
    #
    # ./Examples/Monocular/mono_tum_vi Vocabulary/ORBvoc.txt data/1920x1080_Kilgo1/$threshold.yaml data/1920x1080_Kilgo1/data data/1920x1080_Kilgo1/timestamps.txt k1_1920_t${threshold}_s$seed && 
    # mkdir -p results/k1_1920/$threshold/seed$seed && 
    # mv f_k1_1920_t${threshold}_s${seed}.txt results/k1_1920/$threshold/seed$seed &&
    # mv kf_k1_1920_t${threshold}_s${seed}.txt results/k1_1920/$threshold/seed$seed &&
    # mv keypoints.txt results/k1_1920/$threshold/seed$seed
    # rm keypoints.txt
    # rm f_*
    # rm kf_*


  done 
done 

