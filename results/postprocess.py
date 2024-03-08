import numpy as np 
import argparse 
import associate 
from pprint import pprint 
import matplotlib.pyplot as plt


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
        elif "LOOP" in lines[i+2] and (("G" in lines[i+1]) or ("B" in lines[i+1])): 
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

    return {"good" : above_tracked / total_above, "bad" : below_tracked / total_below}

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
    parser.add_argument("--ground_truth")  
    parser.add_argument("--estimated") 
    parser.add_argument("--keypoints")
    parser.add_argument('--offset', help='time offset added to the timestamps of the second file (default: 0.0)',default=0.0)
    parser.add_argument('--max_difference', help='maximally allowed time difference for matching entries (default: 10000000 ns)',default=20_000_000)

    args = parser.parse_args()

    ground_truth_list = associate.read_file_list(args.ground_truth, False)
    estimated_list = associate.read_file_list(args.estimated, False)

    keypoints = read_keypoints(args.keypoints) 
    matches_gt_est = associate.associate(ground_truth_list, estimated_list,float(args.offset),float(args.max_difference))    

    print(f"Ground Truth : {len(ground_truth_list)} \nEstimated : {len(estimated_list)} \nKeypoints : {len(keypoints)}")

    # should always be the case that len(ground_truth_list) > len(estimated_list) 
    assert len(ground_truth_list) > len(estimated_list)
    ground_truth_list, _, unkept_indices = keep_matched_keys(ground_truth_list, [x[0] for x in matches_gt_est])

    estimated_list, _, _ = keep_matched_keys(estimated_list, [x[1] for x in matches_gt_est])
    matches_est_kp = associate.associate(keypoints, ground_truth_list, float(args.offset), float(args.max_difference))
    filtered_keypoints = {} 
    for match in matches_est_kp:
        filtered_keypoints[match[0]] =  keypoints[match[0]]

    print(f"Ground Truth : {len(ground_truth_list)} \nEstimated : {len(estimated_list)} \nKeypoints : {len(filtered_keypoints)}")

    assert len(ground_truth_list) == len(estimated_list) == len(filtered_keypoints)

    
    loop_closing_indices = get_loop_closing_indices(keypoints)
    for i in range(len(loop_closing_indices) - 1): 
        start = loop_closing_indices[i]
        stop = loop_closing_indices[i+1]
        print(f"Relative Error [{start}, {stop}] : {get_relative_acc_subtraj(ground_truth_list, estimated_list, start, stop, False)}")

    tracked_indices = get_tracked_indices(keypoints)

    print(f"Loop closing indices : {loop_closing_indices}") 
    print(f"Tracking indices : {tracked_indices}") 

    feature_threshold_indices = get_feature_threshold_indices(keypoints, 2300)

    for i in range(len(feature_threshold_indices) - 1): 
        start = feature_threshold_indices[i] 
        stop = feature_threshold_indices[i+1] 

        print(f"Relative Error in [{start}, {stop}] : {get_relative_acc_subtraj(ground_truth_list, estimated_list, start, stop, False)}")

        

    print(feature_threshold_indices)

    print(tracked_indices) 
    print(feature_threshold_indices)



