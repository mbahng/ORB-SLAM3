from re import A
import matplotlib.pyplot as plt 
import numpy as np
from pprint import pprint


def plot_loop_closing(): 

    def get_totalErr_vs_sumOfSubTrajErr(data:list): 
        total_err = data[-1] 
        sum_of_subtraj_err = sum(data[:-1])

        return total_err, sum_of_subtraj_err

    with open("/home/iotlab/Desktop/ORB_SLAM3/plot/loop_closing.txt", "r") as f: 
        data = [eval(line.strip().split(" : ")[-1]) for line in f.readlines()]

    rel_err_change = []
    for elem in data: 
        changes = get_totalErr_vs_sumOfSubTrajErr(elem) 
        rel_err_change.append(changes)


    bad_loop_close = [x[0] for x in rel_err_change if x[0] > x[1]] 
    good_loop_close = [x[0] for x in rel_err_change if x[0] < x[1]] 

    g_mean, g_std = np.mean(good_loop_close), np.std(good_loop_close)
    b_mean, b_std = np.abs(np.mean(bad_loop_close)), np.std(bad_loop_close)

    g_prop = round(len(good_loop_close)/(len(good_loop_close) + len(bad_loop_close)), 2)
    b_prop = round(len(bad_loop_close) / (len(good_loop_close) + len(bad_loop_close)), 2)

    plt.plot()
    plt.bar(
        [f"good ({g_prop})", f"bad ({b_prop})"], 
        [g_mean, b_mean], 
        yerr = [g_std, b_std] 
    )
    plt.title("Total Trajectory Error from Good/Bad Loop Closing") 
    plt.savefig("loop_closing") 

def plot_keypoint_traj_acc(): 
    above, below = [], [] 

    with open("/home/iotlab/Desktop/ORB_SLAM3/plot/keypoint_traj_acc.txt", "r") as f: 
        above = [eval(line.strip().split(" - ")[-1]) for line in f.readlines() if "above" in line] 

    with open("/home/iotlab/Desktop/ORB_SLAM3/plot/keypoint_traj_acc.txt", "r") as f: 
        below = [eval(line.strip().split(" - ")[-1]) for line in f.readlines() if "below" in line] 

    assert len(above) == len(below) 

    above_tmp, below_tmp = [], [] 
    for i in range(len(above)): 
        above_tmp += above[i] 
        below_tmp += below[i]

    # get rid of degenerate cases 
    above = [x for x in above_tmp if x not in [-100, 0.0]]
    below = [x for x in below_tmp if x not in [-100, 0.0]]

    above_mean, above_std = np.mean(above), np.std(above) 
    below_mean, below_std = np.mean(below), np.std(below)

    # log_space = list(np.logspace(0, 2, 50))
    # plt.hist(above, alpha=0.5, label="above threshold", bins=log_space)
    # plt.hist(below, alpha=0.5, label="below threshold", bins=log_space)
    # plt.legend()
    # plt.title("Total Trajectory Error from Above/Below Feature Threshold")
    # plt.savefig("hist")

    plt.bar(
        ["Above", "Below"], 
        [above_mean, below_mean], 
        yerr = [above_std, below_std]
    )
    plt.title("Relative Trajectory Error from Above/Below Feature Threshold")
    plt.savefig("keypoint_traj_acc")

def plot_keypoint_tracked_status(): 
    data = []
    with open("/home/iotlab/Desktop/ORB_SLAM3/plot/keypoint_tracked_status.txt", "r") as f: 
        data = [eval(line.strip().split(" : ")[-1]) for line in f.readlines() if "above" in line] 
    
    above_tracked_percentage = []
    below_tracked_percentage = [] 
    for dct in data: 
        above_tracked_percentage.append((dct['above_tracked'] + 1e-8) / (dct['above_total'] + 1e-8)) 
        below_tracked_percentage.append((dct['below_tracked'] + 1e-8) / (dct['below_total'] + 1e-8)) 

    above_mean, above_std = np.mean(above_tracked_percentage), np.std(above_tracked_percentage)
    below_mean, below_std = np.mean(below_tracked_percentage), np.std(below_tracked_percentage)

    plt.ylim([0.7, 1.0])
    plt.bar(
        ["Above", "Below"], 
        [above_mean, below_mean], 
        yerr = [above_std, below_std]
    )
    plt.title("Average Percent Tracked within Subtracjectories Above/Below Feature Threshold")
    plt.savefig("keypoint_tracked_status")


if __name__ == "__main__": 
    plot_keypoint_tracked_status()
    pass 
