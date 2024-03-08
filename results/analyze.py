import numpy as np 
import argparse 
import associate 
from pprint import pprint 
import matplotlib.pyplot as plt
import warnings 
import os 
import psutil

warnings.filterwarnings("ignore")

DATA_PATH = os.path.join("/", "home", "iotlab", "Desktop", "ORB_SLAM3", "data")
RESULT_PATH = os.path.join("/", "home", "iotlab", "Desktop", "ORB_SLAM3", "results")

def align(model,data):
    """Align two trajectories using the method of Horn (closed-form).
    
    Input:
    model -- first trajectory (3xn)
    data -- second trajectory (3xn)
    
    Output:
    rot -- rotation matrix (3x3)
    trans -- translation vector (3x1)
    trans_error -- translational error per point (1xn)
    """


    np.set_printoptions(precision=3,suppress=True)
    model_zerocentered = model - model.mean(1)
    data_zerocentered = data - data.mean(1)
    
    W = np.zeros( (3,3) )
    for column in range(model.shape[1]):
        W += np.outer(model_zerocentered[:,column],data_zerocentered[:,column])
    U,d,Vh = np.linalg.svd(W.transpose())
    S = np.matrix(np.identity( 3 ))
    if(np.linalg.det(U) * np.linalg.det(Vh)<0):
        S[2,2] = -1
    rot = U*S*Vh

    rotmodel = rot*model_zerocentered
    dots = 0.0
    norms = 0.0

    for column in range(data_zerocentered.shape[1]):
        dots += np.dot(data_zerocentered[:,column].transpose(),rotmodel[:,column])
        normi = np.linalg.norm(model_zerocentered[:,column])
        norms += normi*normi

    s = float(dots/norms)
    
    transGT = data.mean(1) - s*rot * model.mean(1)
    trans = data.mean(1) - rot * model.mean(1)

    model_alignedGT = s*rot * model + transGT
    model_aligned = rot * model + trans

    alignment_errorGT = model_alignedGT - data
    alignment_error = model_aligned - data

    trans_errorGT = np.sqrt(np.sum(np.multiply(alignment_errorGT,alignment_errorGT),0)).A[0]
    trans_error = np.sqrt(np.sum(np.multiply(alignment_error,alignment_error),0)).A[0]
        
    return rot,transGT,trans_errorGT,trans,trans_error, s

def keep_matched_keys(list_file, keys): 
    unkept_times = [] 
    unkept_indices = []
    res = {}
    for i, k in enumerate(list(sorted(list_file.keys()))):
        if k in keys: 
            res[k] = list_file[k] 
        else: 
            unkept_indices.append(i) 
            unkept_times.append(k)

    return res, unkept_times, unkept_indices

def read_keypoints(file): 
    file = open(file) 
    data = file.read()
    lines = data.split("\n") 

    i = 0 
    res = {} 

    while i < len(lines) - 1: 
        detected = "" 
        loop = False 
        stuff = lines[i].strip().split() 
        # print(stuff)

        if "LOOP" in lines[i+1]: 
            loop = True 
            if ("G" in lines[i+2]) or ("B" in lines[i+2]): 
                detected = lines[i+2].strip() 
                i += 3
            else: 
                detected = "G" 
                i += 2
        elif (i < len(lines) - 2) and ("LOOP" in lines[i+2]) and (("G" in lines[i+1]) or ("B" in lines[i+1])): 
            loop = True 
            detected = lines[i+1].strip() 
            i += 3 
        elif ("G" in lines[i+1]) or ("B" in lines[i+1]): 
            detected = lines[i+1].strip()
            i += 2
        else: 
            detected = "G" 
            i += 1 

        key, val = stuff[0], stuff[1] 
        res[int(key)] = (int(val), detected, loop) 
        # print(int(key), " : ", int(val), detected, loop)
            
    return res 

def keep_matched_keypoints(kp_dict, idx_to_remove): 
    res = {} 
    for i, k in enumerate(list(sorted(kp_dict.keys()))): 
        if i not in idx_to_remove: 
            res[k] = kp_dict[k]

    return res

def get_feature_threshold_vs_percent_frames_tracked(keypoint_dict, threshold, verbose=True): 
    total_above, total_below = 0, 0
    above_tracked, below_tracked = 0, 0 


    for key in keypoint_dict.keys(): 
        if keypoint_dict[key][0] < threshold: 
            # then this is bad in feature points 
            total_below += 1 
            if keypoint_dict[key][1] == "G": 
                below_tracked += 1 
            elif keypoint_dict[key][1] == "B": 
                pass
            else: 
                raise Exception("This should not occur") 

        elif keypoint_dict[key][0] >= threshold: 
            total_above += 1 
            if keypoint_dict[key][1] == "G": 
                above_tracked += 1 
            elif keypoint_dict[key][1] == "B": 
                pass
            else: 
                raise Exception("This should not occur") 

        else: 
            raise Exception("This should not occur") 

    if verbose: 
        print(f"Above Threshold Tracked / Total : {above_tracked} / {total_above}")
        print(f"Below Threshold Tracked / Total : {below_tracked} / {total_below}")

    return {
        "above_tracked" : above_tracked, 
        "above_total" : total_above, 
        "below_tracked" : below_tracked, 
        "below_total" : total_below
    }

def get_relative_acc_subtraj(ground_truth_list, estimated_list, start, stop, verbose=True): 
    first_xyz = np.matrix([[float(value) for value in ground_truth_list[k][0:3]] for k in sorted(list(ground_truth_list.keys()))[start:stop]]).transpose()
    second_xyz = np.matrix([[float(value) for value in estimated_list[k][0:3]] for k in sorted(list(estimated_list.keys()))[start:stop]]).transpose()
    first_list = ground_truth_list
    second_list = estimated_list

    dictionary_items = second_list.items()
    sorted_second_list = sorted(dictionary_items)

    second_xyz_full = np.matrix([[float(value) for value in sorted_second_list[i][1][0:3]] for i in range(len(sorted_second_list))]).transpose() # sorted_second_list.keys()]).transpose()
    rot,transGT,trans_errorGT,trans,trans_error, scale = align(second_xyz,first_xyz)
    
    second_xyz_aligned = scale * rot * second_xyz + trans
    second_xyz_notscaled = rot * second_xyz + trans
    second_xyz_notscaled_full = rot * second_xyz_full + trans
    first_stamps = list(first_list.keys())
    first_stamps.sort()
    first_xyz_full = np.matrix([[float(value) for value in first_list[b][0:3]] for b in first_stamps]).transpose()
    
    second_stamps = list(second_list.keys())
    second_stamps.sort()
    second_xyz_full = np.matrix([[float(value) for value in second_list[b][0:3]] for b in second_stamps]).transpose()
    second_xyz_full_aligned = scale * rot * second_xyz_full + trans

    if verbose: 
        print(first_xyz_full)
        print(second_xyz_full_aligned)
        
    # plt.plot(list(np.array(first_xyz_full[0, :])[0]))
    # plt.plot(list(np.array(second_xyz_full_aligned[0, :])[0])) 
    # plt.show()

    error = np.sqrt(np.dot(trans_errorGT,trans_errorGT) / len(trans_errorGT))

    return error

def get_loop_closing_indices(keypoints): 
    indices = [0]
    for i, k in enumerate(sorted(list(keypoints.keys()))): 
        if keypoints[k][2]: 
            indices.append(i) 

    indices.append(len(keypoints))

    return indices

def get_tracked_indices(keypoints): 
    indices = [0] 
    state = "G" 
    for i, k in enumerate(sorted(list(keypoints.keys()))): 
        tracked_state = keypoints[k][1]
        assert tracked_state in ["G", "B"] 
        if tracked_state != state: 
            indices.append(i) 
            state = tracked_state 

    indices.append(len(keypoints)) 

    return indices

def get_feature_threshold_indices(keypoints, threshold): 
    indices = [0] 
    above = True 
    for i, k in enumerate(sorted(list(keypoints.keys()))): 
        above_threshold = keypoints[k][0] > threshold 
        if above_threshold is not above: 
            indices.append(i) 
            above = above_threshold 

    indices.append(len(keypoints)) 

    return indices


if __name__ == "__main__": 
    
    parser = argparse.ArgumentParser() 
    parser.add_argument("--dataset")  
    parser.add_argument("--threshold")  
    parser.add_argument("--seed")  
    parser.add_argument('--offset', help='time offset added to the timestamps of the second file (default: 0.0)',default=0.0)
    parser.add_argument('--max_difference', help='maximally allowed time difference for matching entries (default: 10000000 ns)',default=20_000_000)
    parser.add_argument('--loop_closing', help="If set to true, it outputs the subtrajectory errors between loop closing indices", action="store_true")
    parser.add_argument('--keypoints_vs_accuracy', help="If set to true, it outputs the subtrajectory errors between loop closing indices", action="store_true")
    parser.add_argument('--keypoints_vs_tracking', help="If set to true, it outputs the subtrajectory errors between loop closing indices", action="store_true")
    parser.add_argument('--cpu_mem', help="If set to true, it outputs the subtrajectory errors between loop closing indices", action="store_true")
    args = parser.parse_args()
    datasets = { # ground truth, estimated, keypoints
        "av256m" : [
                os.path.join(DATA_PATH, "256x144_moving", "ground_truth.csv"), 
                os.path.join(RESULT_PATH, "av256m", args.threshold, f"seed{args.seed}", f"f_av256m_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "av256m", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "av256s" : [
                os.path.join(DATA_PATH, "256x144_stationary", "ground_truth.csv"), 
                os.path.join(RESULT_PATH, "av256s", args.threshold, f"seed{args.seed}", f"f_av256s_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "av256s", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "av512m" : [
                os.path.join(DATA_PATH, "512x288_moving", "ground_truth.csv"), 
                os.path.join(RESULT_PATH, "av512m", args.threshold, f"seed{args.seed}", f"f_av512m_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "av512m", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "av512s" : [
                os.path.join(DATA_PATH, "512x288_stationary", "ground_truth.csv"), 
                os.path.join(RESULT_PATH, "av512s", args.threshold, f"seed{args.seed}", f"f_av512s_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "av512s", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "euroc_mh1_752" : [
                os.path.join(DATA_PATH, "MH_01_easy", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_mh1_752", args.threshold, f"seed{args.seed}", f"f_euroc_mh1_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_mh1_752", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "euroc_mh2_752" : [
                os.path.join(DATA_PATH, "MH_02_easy", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_mh2_752", args.threshold, f"seed{args.seed}", f"f_euroc_mh2_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_mh2_752", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "euroc_mh3_752" : [
                os.path.join(DATA_PATH, "MH_03_medium", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_mh3_752", args.threshold, f"seed{args.seed}", f"f_euroc_mh3_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_mh3_752", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "euroc_mh4_752" : [
                os.path.join(DATA_PATH, "MH_04_difficult", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_mh4_752", args.threshold, f"seed{args.seed}", f"f_euroc_mh4_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_mh4_752", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "euroc_mh5_752" : [
                os.path.join(DATA_PATH, "MH_05_difficult", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_mh5_752", args.threshold, f"seed{args.seed}", f"f_euroc_mh5_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_mh5_752", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "euroc_v101_752" : [
                os.path.join(DATA_PATH, "V1_01_easy", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_v101_752", args.threshold, f"seed{args.seed}", f"f_euroc_v101_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_v101_752", args.threshold, f"seed{args.seed}", f"keypoints.txt")
                ], 
        "euroc_v102_752" : [
                os.path.join(DATA_PATH, "V1_02_medium", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_v102_752", args.threshold, f"seed{args.seed}", f"f_euroc_v102_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_v102_752", args.threshold, f"seed{args.seed}", f"keypoints.txt")
                ], 
        "euroc_v103_752" : [
                os.path.join(DATA_PATH, "V1_03_difficult", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_v103_752", args.threshold, f"seed{args.seed}", f"f_euroc_v103_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_v103_752", args.threshold, f"seed{args.seed}", f"keypoints.txt")
                ], 
        "euroc_v201_752" : [
                os.path.join(DATA_PATH, "V2_01_easy", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_v201_752", args.threshold, f"seed{args.seed}", f"f_euroc_v201_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_v201_752", args.threshold, f"seed{args.seed}", f"keypoints.txt")
                ], 
        "euroc_v202_752" : [
                os.path.join(DATA_PATH, "V2_02_medium", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_v202_752", args.threshold, f"seed{args.seed}", f"f_euroc_v202_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_v202_752", args.threshold, f"seed{args.seed}", f"keypoints.txt")
                ], 
        "euroc_v203_752" : [
                os.path.join(DATA_PATH, "V2_03_difficult", "mav0", "state_groundtruth_estimate0", "data.csv"), 
                os.path.join(RESULT_PATH, "euroc_v203_752", args.threshold, f"seed{args.seed}", f"f_euroc_v203_752t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "euroc_v203_752", args.threshold, f"seed{args.seed}", f"keypoints.txt")
                ], 
        "k1_1920" : [
                os.path.join(DATA_PATH, "1920x1080_Kilgo1"), 
                os.path.join(RESULT_PATH, "k1_1920", args.threshold, f"seed{args.seed}", f"f_k1_1920_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "k1_1920", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "kb960" : [
                os.path.join(DATA_PATH, "960x720_KilgoB1"), 
                os.path.join(RESULT_PATH, "kb960", args.threshold, f"seed{args.seed}", f"f_kb960_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "kb960", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "tum_room1_512" : [
                os.path.join(DATA_PATH, "dataset-room1_512_16", "mav0", "mocap0", "data.csv"), 
                os.path.join(RESULT_PATH, "tum_room1_512", args.threshold, f"seed{args.seed}", f"f_tum_rm1_512_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "tum_room1_512", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "tum_room2_512" : [
                os.path.join(DATA_PATH, "dataset-room2_512_16", "mav0", "mocap0", "data.csv"), 
                os.path.join(RESULT_PATH, "tum_room2_512", args.threshold, f"seed{args.seed}", f"f_tum_rm2_512_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "tum_room2_512", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "tum_room3_512" : [
                os.path.join(DATA_PATH, "dataset-room3_512_16", "mav0", "mocap0", "data.csv"), 
                os.path.join(RESULT_PATH, "tum_room3_512", args.threshold, f"seed{args.seed}", f"f_tum_rm3_512_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "tum_room3_512", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "tum_room4_512" : [
                os.path.join(DATA_PATH, "dataset-room4_512_16", "mav0", "mocap0", "data.csv"), 
                os.path.join(RESULT_PATH, "tum_room4_512", args.threshold, f"seed{args.seed}", f"f_tum_rm4_512_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "tum_room4_512", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "tum_room5_512" : [
                os.path.join(DATA_PATH, "dataset-room5_512_16", "mav0", "mocap0", "data.csv"), 
                os.path.join(RESULT_PATH, "tum_room5_512", args.threshold, f"seed{args.seed}", f"f_tum_rm5_512_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "tum_room5_512", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
        "tum_room6_512" : [
                os.path.join(DATA_PATH, "dataset-room6_512_16", "mav0", "mocap0", "data.csv"), 
                os.path.join(RESULT_PATH, "tum_room6_512", args.threshold, f"seed{args.seed}", f"f_tum_rm6_512_t{args.threshold}_s{args.seed}.txt"), 
                os.path.join(RESULT_PATH, "tum_room6_512", args.threshold, f"seed{args.seed}", "keypoints.txt")
                ], 
    }
    assert args.dataset in datasets.keys()
    ground_truth_list = associate.read_file_list(datasets[args.dataset][0], False)
    estimated_list = associate.read_file_list(datasets[args.dataset][1], False)
    keypoints = read_keypoints(datasets[args.dataset][2]) 
    matches_gt_est = associate.associate(ground_truth_list, estimated_list,float(args.offset),float(args.max_difference))    
    assert len(ground_truth_list) > len(estimated_list)
    ground_truth_list, _, unkept_indices = keep_matched_keys(ground_truth_list, [x[0] for x in matches_gt_est])
    estimated_list, _, _ = keep_matched_keys(estimated_list, [x[1] for x in matches_gt_est])
    matches_est_kp = associate.associate(keypoints, ground_truth_list, float(args.offset), float(args.max_difference))
    filtered_keypoints = {} 
    for match in matches_est_kp:
        filtered_keypoints[match[0]] =  keypoints[match[0]]
    assert len(ground_truth_list) == len(estimated_list) == len(filtered_keypoints)

    if args.loop_closing: 
        loop_closing_indices = get_loop_closing_indices(keypoints)
        # print(f"Loop closing indices : {loop_closing_indices}") 
        loop_traj_errors = []
        for i in range(len(loop_closing_indices) - 1): 
            start = loop_closing_indices[i]
            stop = loop_closing_indices[i+1]
            # print(f"Relative Error [{start}, {stop}] : {get_relative_acc_subtraj(ground_truth_list, estimated_list, start, stop, False)}")
            try: 
                rel_traj_err = get_relative_acc_subtraj(ground_truth_list, estimated_list, start, stop, False)
            except: 
                rel_traj_err = -1
            loop_traj_errors.append(round(rel_traj_err * 100, 5))
        loop_traj_errors.append(round(get_relative_acc_subtraj(ground_truth_list, estimated_list, 0, loop_closing_indices[-1], False) * 100, 5))

        print(f"{args.dataset}/{args.threshold}/{args.seed} : {loop_traj_errors}")

    elif args.keypoints_vs_accuracy: 
        feature_threshold_indices = get_feature_threshold_indices(keypoints, 0.8 * float(args.threshold))  

        errors_above_threshold, errors_below_threshold = [], []
        even = True 
        for i in range(len(feature_threshold_indices) - 1): 
            start = feature_threshold_indices[i] 
            stop = feature_threshold_indices[i+1] 
            rel_traj_err = 0.

            if stop - start > 2: 
                try: 
                    rel_traj_err = get_relative_acc_subtraj(ground_truth_list, estimated_list, start, stop, False) 
                except: 
                    rel_traj_err = -1 
            else: 
                rel_traj_err = -1

            if even: 
                even = False 
                if not np.isnan(rel_traj_err): 
                    errors_above_threshold.append(round(rel_traj_err * 100, 5)) 
            else: 
                even = True 
                if not np.isnan(rel_traj_err): 
                    errors_below_threshold.append(round(rel_traj_err * 100, 5))

        errors_above_threshold = [x for x in errors_above_threshold if x != -100]
        errors_below_threshold = [x for x in errors_below_threshold if x != -100]

        print(f"{args.dataset}/{args.threshold}/{args.seed} : above - {errors_above_threshold}")
        print(f"{args.dataset}/{args.threshold}/{args.seed} : below - {errors_below_threshold}")
       
    elif args.keypoints_vs_tracking: 
        res = get_feature_threshold_vs_percent_frames_tracked(keypoints, 0.8 * float(args.threshold), False)
        print(f"{args.dataset}/{args.threshold}/{args.seed} : {res}")

    elif args.cpu_mem: 
        cpu_usage = psutil.cpu_percent(interval=1) # You can specify the interval in seconds 
        memory_usage = psutil.virtual_memory().percent
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")

