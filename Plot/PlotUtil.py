
from Util import *


"""
    read data from file of this experiment.

    return orig_x, x, contro_switch
"""
def read_data(filename):
    # data format (orig_x, x, contro_switch, failed_switch_loc, flow_switch)
    matrix = np.loadtxt(filename, dtype=np.int)
    orig_x = matrix[0].tolist()
    x = matrix[1].tolist()
    contro_swtich = matrix[2:2 + len(matrix[0])].tolist()
    failed_switch_loc = matrix[2 + len(matrix[0])].tolist()
    flow_switch = matrix[2 + len(matrix[0]) + 1:]
    return orig_x, x, contro_swtich, failed_switch_loc, flow_switch


"""
    calculate the original controllers
"""
def cal_control(contro_switch):
    length = len(contro_switch)

    controllers = []
    for i in range(length):
        if sum(contro_switch[i]) == 0:
            continue
        controllers.append(i)
    return controllers

"""
    calculate the live controllers
"""
def cal_live_control(contro_switch, orig_x):

    switch_contro = matrix_transpose(contro_switch)
    zero_list = [0 for i in range(len(orig_x))]

    for i in range(len(orig_x)):
        if orig_x[i] == 0:
            switch_contro[i] = zero_list
    new_contro_switch = matrix_transpose(switch_contro)
    return cal_control(new_contro_switch)

"""
    calculate the flow set of a switch
    switch_id: the id of switch
    flow_switch: the flow switch map matrix
    
    return the flow set
"""
def cal_switch_flow(switch_id, flow_switch):
    flow_set = set()
    switch_flow = matrix_transpose(flow_switch)

    for flow_id in range(len(switch_flow[switch_id])):
        if switch_flow[switch_id][flow_id] == 0:
            continue
        flow_set.add(flow_id)
    return flow_set


"""
    calculate flow numbers of each controller
    contro_switch: the current controller and switch map matrix
    flow_switch: the flow and switch map matrix
    
    return: the (controller_id, flow_set, countflownum) tuple list
"""
def cal_control_flownum(contro_switch, flow_switch):

    res_tpl_list = []
    for i in range(len(contro_switch)):
        if sum(contro_switch[i]) == 0:
            continue
        flow_set = set()
        count = 0
        for j in range(len(contro_switch[i])):
            if contro_switch[i][j] == 0:
                continue
            tmp_flow = cal_switch_flow(j, flow_switch)
            flow_set |= tmp_flow
            count += len(tmp_flow)

        res_tpl_list.append((i, flow_set, count))

    return res_tpl_list


"""
    calculate the recovered switch id list
    ori_x: switch availability vector after failing
    new_x: switch availability vector after recovering
    
    return: the recovered_switch list
"""
def cal_recovered_switch(ori_x, new_x):

    recovered_switch = []

    for i in range(len(ori_x)):
        if ori_x[i] == 0 and new_x[i] == 1:
            recovered_switch.append(i)
    return recovered_switch


"""
    calculate the recovered switch flow
    return: the (switch_id, flow_set) tuple list
"""
def cal_switchs_flow_list(recovered_switch, flow_switch):

    res_tpl_list = []
    for switch_id in recovered_switch:
        flow_set = cal_switch_flow(switch_id, flow_switch)
        res_tpl_list.append((switch_id, flow_set))
    return res_tpl_list

"""
    calculate the failed switches
    orig_x: witch availability vector after failing
"""
def cal_failed_switch(orig_x):

    failed_switch = []
    for i in range(len(orig_x)):
        if orig_x[i] == 0:
            failed_switch.append(i)
    return failed_switch


"""
    calculate the recovered flow percentage
    orig_x: witch availability vector after failing
    new_x: switch availability vector after recovering
    flow_switch: the flow switch map matrix
    
    return: sum percentage, real percentage 
"""
def cal_recovered_flow_percentage(orig_x, new_x, flow_switch):
    failed_switches = cal_failed_switch(orig_x)
    recover_switches = cal_recovered_switch(orig_x, new_x)

    failed_switch_flow_list = cal_switchs_flow_list(failed_switches, flow_switch)
    recovd_switch_flow_list = cal_switchs_flow_list(recover_switches, flow_switch)

    failed_flows_set = set()
    recover_flows_set = set()

    failed_count = 0
    for item in failed_switch_flow_list:
        failed_flows_set |= item[1]
        failed_count += len(item[1])

    recoverd_count = 0
    for item in recovd_switch_flow_list:
        recover_flows_set |= item[1]
        recoverd_count += len(item[1])

    return (float(recoverd_count) / failed_count), (len(recover_flows_set) / float(len(failed_flows_set)))


"""
    calculate the switch number of each live controller
    contro_switch: the controller and switch map matrix
    
    return: (controller_id, switch_num) tuple list 
"""
def cal_control_switch_num(contro_switch):
    res_list = []

    for i in range(len(contro_switch)):
        if sum(contro_switch[i]) > 0:
            res_list.append((i, sum(contro_switch[i])))

    return res_list

"""
    calculate the recovered final object score
    contro_switch: the contoller switch mapping matrix
    w: the weight matrix
    failed_controller: the failed controller list
"""
def cal_recovered_object(contro_switch, w, failed_switch):
    sum_mul = 0
    switch_contro = matrix_transpose(contro_switch)
    for i in range(len(switch_contro)):
        if i not in failed_switch:
            continue
        for j in range(len(switch_contro[i])):
            if switch_contro[i][j] == 0:
                continue
            else:
                sum_mul += (w[i][j] * switch_contro[i][j])
                break

    return sum_mul


"""
    cal near algorithm index
    algnames: sorted algname list
    return: the index of near
"""
def cal_near_index(algnames):
    index = 0
    for i in range(len(algnames)):
        if algnames[i] == 'near':
            index = i
    return index

"""
    calculate the obj lists to the ratio of near
    obj_list: the calculated obj list with 2 level
                the first level is the algorithm
                the inner level is the combination or ratio
    return: the obj ratio list with the same structure
"""
def cal_objratio_list(obj_list, near_index):
    np_near_vector = np.asarray(obj_list[near_index], dtype=np.float)
    res_list = []
    for item in obj_list:
        np_vector = np.asarray(item, dtype=np.float)
        np_ratio_vector = np.divide(np_vector, np_near_vector) * 100.0
        res_list.append(np_ratio_vector.tolist())

    return res_list


"""
    calculate the failed controller remapped controller
    failed_switch: the failed switch list
    contro_switch: the controller switch mapping matrix
    filename: the name of the saved file
"""
def cal_remap(failed_switch, contro_switch, filename):
    z = matrix_transpose(contro_switch)

    with open(filename, 'w') as f:
        for i in failed_switch:
            for j in range(len(z[i])):
                if z[i][j] == 0:
                    continue
                else:
                    f.write('%s->%s\n' % (i, j))
                    break

        f.close()

"""
    save obj to file
    obj: the obj value
    filename: the name of the file
"""

def write_obj(obj, filename):

    with open(filename, 'w') as f:
        f.write('%s' % obj)

    f.close()



