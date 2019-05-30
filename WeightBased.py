from Util import *
import copy


"""
    Place the failed switches in a weight first based way
    
    first sort by flow
    second sort by w
    
    weight: the weight matrix of switch and controller
    z: the switch controller map matrix
    n: the Network object.
"""
def weight_based(weight, failed_switch, n, live_controller, a_rest, ratio):

    # initialize the variables
    x = [1 for i in range(len(n.nodes_dict))]
    failed_d = [0 for i in range(len(n.flows_dict))]  # vector flow num
    d = copy.deepcopy(failed_d)
    z = np.zeros((len(x), len(x)), dtype=np.int).tolist()
    A_rest = copy.deepcopy(a_rest)

    failed_switch_flow = []
    for i in failed_switch:
        x[i] = 0
        tmp_flow = cal_switch_flows(i, n)
        failed_switch_flow.append((i, len(tmp_flow)))
        for elem in tmp_flow:
            failed_d[elem] = 1
    failed_switch_flow.sort(key=lambda t: t[1], reverse=True)

    for (i, _) in failed_switch_flow:
        if sum(d) > sum(failed_d) * ratio:
            return x, d, z
        if x[i] == 1:
            continue

        weight_tpl_list = []
        switch_flow = cal_switch_flows(i, n)
        switch_flow_num = len(switch_flow)
        for j in live_controller:
            weight_tpl_list.append((j, weight[i][j]))
        weight_tpl_list.sort(key=lambda t: t[1])

        for item in weight_tpl_list:
            contro_id = item[0]

            if switch_flow_num > A_rest[contro_id]:
                continue

            else:
                A_rest[contro_id] -= switch_flow_num
                z[i][contro_id] = 1
                x[i] = 1
                for elem in switch_flow:
                    d[elem] = 1
                break

    return x, d, z



