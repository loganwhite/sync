import random
from math import radians

from igraph import *
from Entity import *
import ast
import numpy as np
import copy
import math



'''
    find_max, find the maximum value of 
    a list l and return both the max value and its index

    l: the list

    return: max_value, max_index
'''
def find_max(l):
    max_value = max(l)
    return max_value, l.index(max_value)
    
'''
    find_min, find the minimum value of 
    a list l and return both the min value and its index

    l: the list

    return: min_value, min_index
'''
def find_min(l):
    if len(l) == 0:
        return []
    min_value = min(l)
    return min_value, l.index(min_value)

"""
    get central vertex id of the igraph object g

    g: the igraph object
    return: the vertex_id value
"""
def get_central_point(g):
    vs = VertexSeq(g)

    distance_matrix = g.shortest_paths_dijkstra()

    vertex_score_list = []
    for v in vs:
        score = 0
        for s in vs:
            s_id = int(s["id"])
            v_id = int(v["id"])
            if s_id != v_id:
                score += distance_matrix[s_id][v_id]
        vertex_score_list.append(score)
    
    return find_min(vertex_score_list)


"""
    group vertex into n small group
    g: the igraph object
    num: the number of groups 

    return: group list, each goup is a vertex id list.
"""
def group_vertics(g, num):
    vs = VertexSeq(g)

    vs_number = len(vs)

    v_n = int(vs_number / num)

    v_rest = vs_number % num
    v_rest_old = v_rest

    group_list = []

    tmp = []
    for i in range(0, vs_number):
        tmp.append(i)

    # balanced grouping, if there are remaining, put one more elements
    # on the group
    for i in range(num):
        if i == (num-1):
            tmp_group = tmp[i * v_n + v_rest_old:]
        else:
            if v_rest > 0:
                tmp_group = tmp[i * v_n+i: (i + 1) * v_n + 1 +i]
                v_rest -= 1
            else:
                tmp_group = tmp[i * v_n + v_rest_old: (i + 1) * v_n + v_rest_old]

        group_list.append(tmp_group)

    return group_list


"""
    get central vertex of a given group list
    g:      the igraph object
    group:  vertices of group

    return: the central node id
"""

def find_central_of_group(g, group):
    length_list = []
    for i in group:
        score = 0
        for j in group:
            if (i != j):
                score += g.shortest_paths_dijkstra(i, j)[0][0]
        if score != None or score != 0:
            length_list.append(score)
    # return the index
    m = find_min(length_list)
    return group[m[1]]
            


"""
    get the central vertex for each groups
    g:              the igraph object
    group_list :    the group list, each element is a vertex list in the group

    return:         a list of central nodes of each group
"""
def find_central_vertex_groups(g, goups_list):
    central_list = []

    for group in goups_list:
        # sub_vertex = g.vs.select(id in group)
        # sub_graph = g.subgraph(sub_vertex)
        # print("subgraph:",sub_graph)

        # central_list.append(get_central_point(sub_graph))

        central_list.append(find_central_of_group(g, group))


    return central_list


"""
    extract traffic matrix from a single traffic matrix line.

    line: a line of number in the Abilene dataset

    return: matrix

"""

def extract_matrix(line):
    line_array = line.split()

    # print(len(line_array))

    matrix = []
    tmp_row = []
    for i in range(0, 144):
        tmp_row.append(float(line_array[i*5]))
        if ((i+1) % 12) == 0:
            # starting a new row        
            matrix.append(tmp_row)
            tmp_row = []

    return matrix



"""
    read the traffic matrix from a file and return the matrix
    filename: file name of traffic matrix file

    return: matrix list of traffic [[[][]][[][]]]
"""
def read_traffic(filename, traffic_factor):
    matrix_list = []

    with open(filename, "r") as f:
        for line in f:
            
            matrix = extract_matrix(line)
            n = len(matrix)
            for i in range(n):
                for j in range(n):
                    matrix[i][j] = matrix[i][j] *100*8/300/1000 * traffic_factor
            matrix_list.append(matrix)

            
            # for test use
            #break

    
    return matrix_list

"""
    find all the path between 2 nodes

    g: the igraph object
    start: the starting nodes
    end: the end nodes
    vn: the intermedian nodes

    return: paths list
"""
def find_all_paths2(g, start, end, vn = []):
    vn = vn if type(vn) is list else [vn]
    # vn = list(set(vn)-set([start,end]))
    path = []
    paths = []
    queue = [(start, end, path)]
    while queue:
        start, end, path = queue.pop()
        path = path + [start]

        if start not in vn:
            for node in set(g.neighbors(start, mode='OUT')).difference(path):
                queue.append((node, end, path))

            if start == end and len(path) > 0:
                paths.append(path)
            else:
                pass
        else:
            pass

    return paths

def get_path_weight(node_list,link_weight_dict):
    path_weight = 0
    n = len(node_list)
    for i in range(n - 1):
        m = node_list[i]
        n = node_list[i + 1]
        path_weight += link_weight_dict[(min(node_list[i], node_list[i+1]), max(node_list[i], node_list[i+1]))]
    return path_weight


"""
    find all the paths of a given network and store them into the file for further use
    member variable
    n: the Net object
    g: the igraph object, used to pass to the find_all_path2
"""
def find_all_paths_to_file(n, g, filename):
    vs = VertexSeq(g)
    path_id = 0
    f = open(filename, 'w')

    for i in vs:
        # i_id = int(i["id"]) # formal expresion
        i_id = i.index
        for j in vs:
            # j_id = int(j["id"]) # formal expression
            j_id = j.index
            if i_id == j_id:
                continue
            # paths_list = find_all_paths2(g, i_id, j_id, link_weight_dict)
            paths_list = g.get_all_shortest_paths(i_id, j_id)

            # remove duplications
            paths_list = [tuple(path) for path in paths_list]
            paths_list = list(set(paths_list))
            for i in range(len(paths_list)):
                paths_list[i] = list(paths_list[i])

            # judge if the number of paths in paths list is bigger than 5
            # filter the duplications
            if len(paths_list) < 5:
                backup_paths_list = find_all_paths2(g, i_id, j_id)
                backup_paths_list =[path for path in backup_paths_list
                                      if path not in paths_list]
                if len(backup_paths_list) > 0:
                    paths_list += backup_paths_list[:(5-len(paths_list))]

            # replace the renumbered id to the actual id
            for i in range(len(paths_list)):
                for j in range(len(paths_list[i])):
                    renumbered_id = int(paths_list[i][j])
                    paths_list[i][j] = vs[renumbered_id]['id']

            for p in paths_list:
                # get the links from head to tail
                link_list = []
                for i in range(len(p) - 1):
                    link_list.append(n.linkID_dict[(p[i], p[i+1])])

                n.paths_dict[path_id] = Path(path_id, vs[i_id]['id'], vs[j_id]['id'], p, link_list)
                path_id += 1


                f.write("%s-%s-%s-\n" % (vs[i_id]['id'], vs[j_id]['id'], paths_list))
    f.close()


    # with open('path.log.'+ n.topo,'w') as f:
    #
    #     for i in vs:
    #         # i_id = int(i["id"]) formal expresion
    #         i_id = i.index
    #         for j in vs:
    #             # j_id = int(j["id"]) formal expression
    #             j_id = j.index
    #             # paths_list = find_all_paths2(g, i_id, j_id, link_weight_dict)
    #             paths_list = g.get_all_shortest_paths(i_id, j_id)
    #             # format (src, dst, paths_list)
    #             f.write("%s-%s-%s-\n" % (i_id, j_id, paths_list))
    #     f.close()
    #
    # find_all_paths(n, g, link_weight_dict)


"""
    find all the paths of a given network and store them into the file for further use
    member variable
    n: the Net object
    g: the igraph object, used to pass to the find_all_path2
"""


def get_all_paths_from_file(n):

    res_dict = dict()
    print n.name
    with open(n.name, 'r') as f:
        for line in f:
            str_list = line.split('-')
            str_list.remove('\n')
            paths_list = ast.literal_eval(str_list[2])
            # using int(float(x)) to avoid the string is a floating number
            # and cannot be convert to int directly
            res_dict[(int(float(str_list[0])), int(float(str_list[1])))] = paths_list

        f.close()

    return res_dict

    
"""
    find all the paths of a given network and store them into the path_dict
    member variable
    n: the Net object
    g: the igraph object, used to pass to the find_all_path2
"""
def find_all_paths(n, g):
    all_path_dict = get_all_paths_from_file(n)
    vs = VertexSeq(g)
    path_id = 0

    for i in vs:
        i_id = int(i["id"])
        for j in vs:
            j_id = int(j["id"])
            # paths_list = find_all_paths2(g, i_id, j_id, link_weight_dict)
            if (i_id, j_id) not in all_path_dict:
                continue

            paths_list = all_path_dict[(i_id, j_id)]
            for p in paths_list:
                # get the links from head to tail
                link_list = []
                for i in range(len(p) - 1):
                    link_list.append(n.linkID_dict[(p[i], p[i+1])])

                n.paths_dict[path_id] = Path(path_id, i_id, j_id, p, link_list)
                path_id += 1

"""
    generate flow between 2 nodes

    net: the Net object
    src: the source node
    dst: the destination node

    return the newly generated Flow object
"""
def gen_flow_2(net, src, dst, flow_id):
    path_list = []
    for k, v in net.paths_dict.iteritems():
        if v.src == src and v.dst == dst:
            path_list.append(k)

    if len(path_list) > 0:
        shortest_path_list = []

        for path_id in path_list:
            path = net.paths_dict[path_id]
            distance = 0
            for link in path.links:
                distance += net.links_dict[link].dist
            shortest_path_list.append((path_id, distance))
        shortest = min(shortest_path_list, key=lambda t: t[1])

        flow = Flow(flow_id, src, dst, 0, path_list, cur_path_id = shortest[0], distance=shortest[1])
    else:
        flow = None
    return flow


"""
    Genrate all the flows of a given Net object and save 'em into the flows_dict member variable

    net: The net object
"""
def gen_flow_all(net, k, m):

    flow_id = 0
    for k_n, v_n in net.nodes_dict.iteritems():
        for k_m, v_m in net.nodes_dict.iteritems():
            f = gen_flow_2(net, k_n, k_m, flow_id)
            
            if f != None:
                f.get_k_path(net.paths_dict, net.links_dict, k, m)
                net.flows_dict[flow_id] = f
                net.flowID_dict[(k_n, k_m)] = flow_id
                flow_id += 1

"""
    Generate flow in each contoller controlled area
    net: the network object
    group_list: the list of each group
"""
def gen_area_flow_all(net, group_list):
    flow_id = 0
    for group in group_list:
        for i in group:
            for j in group:
                f = gen_flow_2(net, i, j, flow_id)

                if f != None:
                    net.flows_dict[flow_id] = f
                    net.flowID_dict[(i, j)] = flow_id
                    flow_id += 1

            
def matrix_transpose(matrix):
    np_matrix = np.asarray(matrix, dtype=np.int)
    np_trans = np_matrix.transpose()
    return np_trans.tolist()









"""
    calculate the flows for each switch
    switch_id: the id of switch
    n: the network object
    
    return: the flow_id set
"""
def cal_switch_flows(switch_id, n):
    flowid_set = set()

    for f_k, f_v in n.flows_dict.iteritems():
        path = n.paths_dict[f_v.cur_path_id]

        if switch_id in path.nodes:
            flowid_set.add(f_k)

    return flowid_set


"""
    calculate the flows for each switch, exclude the case where switch is the last node of the flow
    switch_id: the id of switch
    n: the network object

    return: the flow_id set
"""


def cal_switch_flows_nolast(switch_id, n):
    flowid_set = set()

    for f_k, f_v in n.flows_dict.iteritems():
        path = n.paths_dict[f_v.cur_path_id]

        # the second condition guarantees the switch should not be the last.
        if switch_id in path.nodes and switch_id != path.nodes[len(path.nodes) - 1]:
            flowid_set.add(f_k)

    return flowid_set

"""
    calculate all load of each controller
"""
def cal_load_each(topo, contro_switch):
    res_dict = dict()
    with open('path.log.' + topo, 'r') as f:
        for line in f:
            str_list = line.split('-')
            str_list.remove('\n')
            paths_list = ast.literal_eval(str_list[2])
            res_dict[(int(str_list[0]), int(str_list[1]))] = paths_list

        f.close()

    result_list = []
    switch_num = len(contro_switch[0])

    for i in range(len(contro_switch)):
        if sum(contro_switch[i]) == 0:
            continue
        count = 0
        for j in range(len(contro_switch[i])):
            if contro_switch[j] == 1:
                count += cal_load_each(topo, switch_num, res_dict)
        result_list.append((i, count))
    return result_list

"""
    calculate the failed switch number
"""
def cal_failed_switch_num(contro_switch):
    np_contro_switch = np.asarray(contro_switch)

    np_switch_contro = np_contro_switch.transpose()
    switch_contro = np_switch_contro.tolist()

    count = 0

    for i in switch_contro:
        if sum(i) == 0:
            count += 1
    return count

"""
    calculate the number of recovered flows
    
    recovered_swith: the recovered switch list
    flow_switch: the relationship between flows and switch
    
    return: the number of reccoverd flows
"""
def cal_recovered_flows(recovered_switch, flow_switch):
    switch_flow = matrix_transpose(flow_switch)

    rec_flow_set = set()
    for i in recovered_switch:
        for j in range(len(switch_flow[i])):
            if switch_flow[i][j] == 1:
                rec_flow_set.add(j)

    return len(rec_flow_set)


"""
    group the switch according to flows
    node_list: the node flows list in the format of (node_id, flow_num)
    num: the number of groups
    
    return: the group list
"""
# def group_switch_flow(node_list, num):
#     switch_num = len(node_list)
#     member_num = switch_num / float(num)
#     remainder = switch_num % num
#
#     node_list.sort(key=lambda t: t[1])
#
#     # put the remainders to the rear groups, each by 1
#     group_list = []
#     group = []
#     # the iterator, choose from the head and the tail each at a time.
#     i = 0
#     for group_i in range(num):
#         # for each group, the
#         for i in range(switch_num / 2):
#             # the front groups
#             if group_i < (switch_num - remainder):
#                 if len(group) == member_num:
#                     group_list.append(group)
#                     group = []
#                 else:
#                     for mem_i in range(member_num):


"""
    calculate the line distance matrix of switch pair
    n: the network object
    
    return: the distance matrix
"""
def cal_distance_matrix(n):
    num = len(n.nodes_dict)

    dis_matrix = []
    for i in range(num):
        node_i = n.nodes_dict[i]
        tmp = [0 for x in range(num)]
        for j in range(num):
            if i != j:
                node_j = n.nodes_dict[j]
                distance = math.sqrt((node_i.longi - node_j.longi) ** 2.0
                                     + (node_i.lati - node_j. lati) ** 2.0)
                tmp[j] = distance
        dis_matrix.append(tmp)
    return dis_matrix

"""
    find cluster groups. find the groups whose nodes are 
    the most close
    matrix: the distance matrix.
    group_num: the number of groups
    
    return: the group_list
"""
def cal_cluster_group(matrix, group_num, ability, n):
    switch_num = len(matrix)
    member_num = switch_num / group_num
    remainder = switch_num % group_num

    node_set = set()
    for i in range(switch_num):
        node_set.add(i)
    group_list = []
    # for group_i in range(group_num):
    while len(node_set) > 0:
        group = []
        flow_set = set()
        count = 0
        if len(node_set) == 0:
            break
        src_elem = node_set.pop()
        # put the first element into the group
        group.append(src_elem)
        flow_set |= cal_switch_flows(src_elem, n)
        count += len(cal_switch_flows(src_elem, n))

        tup_list = []
        for i in range(switch_num):
            if i != src_elem and i in node_set:
                tup_list.append((i, matrix[src_elem][i]))
        tup_list.sort(key=lambda t: t[1])


        if remainder > 0:
            # the first element have already put into the list
            for i in range(len(tup_list)):
                tmp_flow_set = copy.deepcopy(flow_set)
                tmp_flow_set |= cal_switch_flows(tup_list[i][0], n)
                tmp_count = count
                tmp_count += len(cal_switch_flows(tup_list[i][0], n))

                # if len(tmp_flow_set) <= ability and len(group) <= member_num:
                if tmp_count <= ability and len(group) <= member_num:
                    flow_set = copy.deepcopy(tmp_flow_set)
                    count = tmp_count
                    group.append(tup_list[i][0])
                    node_set.remove(tup_list[i][0])
                else:
                    break
        else:
            # the first element have already put into the list
            for i in range(len(tup_list)):
                tmp_flow_set = copy.deepcopy(flow_set)
                tmp_flow_set |= cal_switch_flows(tup_list[i][0], n)

                tmp_count = count
                tmp_count += len(cal_switch_flows(tup_list[i][0], n))
                # the second condition without =
                # if len(tmp_flow_set) <= ability and len(group) < member_num:
                if tmp_count <= ability and len(group) < member_num:
                    flow_set = copy.deepcopy(tmp_flow_set)
                    count = tmp_count
                    group.append(tup_list[i][0])
                    node_set.remove(tup_list[i][0])
                else:
                    break
        group_list.append(group)
    return group_list


"""
    Calculate the Ability rest list of controllers
    a: the ability
    n: the network object
    contro_switch: the controller switch map
    return: ability list
"""
def cal_a_rest(a, n, contro_switch):
    A_rest = [0 for i in range(len(contro_switch))]
    for i in range(len(contro_switch)):
        if sum(contro_switch[i]) == 0:
            continue

        counter = 0
        flows = set()
        for j in range(len(contro_switch[i])):
            if contro_switch[i][j] == 1:
                tmp_flow = cal_switch_flows(j, n)
                counter += len(tmp_flow)
                flows |= tmp_flow
        A_rest[i] = a - counter

    return A_rest

"""
    calculate the alibity rest list of controllers,
    for each flow, the last switch is not taken into account
    a: the ability
    n: the network object
    contro_switch: the controller_switch map
    return: the A rest no last list
"""
def cal_a_rest_nolast(a, n, contro_switch):
    A_rest_nolast = [0 for i in range(len(contro_switch))]

    for i in range(len(contro_switch)):
        if sum(contro_switch[i]) == 0:
            continue

        counter = 0
        flows = set()
        for j in range(len(contro_switch[i])):
            if contro_switch[i][j] == 1:
                tmp_flow = cal_switch_flows_nolast(j, n)
                counter += len(tmp_flow)
                flows |= tmp_flow
        A_rest_nolast[i] = a - counter
        # A_rest_nolast[i] = a - len(flows)

    return A_rest_nolast


"""
    sort the weight matrix
    w: the weight matrix
    return: a tuple list list where each elem is a sorted tuple list in the format of (contro_id, weight)
            the sort is based on weight and in ascend way.
"""
def sort_weight(w):
    res_list = []

    for i in range(len(w)):
        tpl_list = []
        for j in range(len(w[i])):

            tpl_list.append((j, w[i][j]))
        tpl_list.sort(key=lambda t: t[1])
        res_list.append(tpl_list)
    return res_list

"""
    round the precision
    for a given matrix, round the number to 0 or 1
    matrix: the input matrix
    return: the rounded matrix
"""
def round_matrix(matrix):
    res_matrix = []
    for i in range(len(matrix)):
        tmp_list = []
        for j in range(len(matrix[i])):
            tmp_list.append(int(round(matrix[i][j])))
        res_matrix.append(tmp_list)

    return res_matrix


"""
    calculate distance from latitude and langitude
"""
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert from decimal to arc
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine equation
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r * 1000


""""
    check list1 is a sublist of list2
    list1: list
    list2: list
    
    return: true if list1 is a sublist of list2, false otherwise
"""
def is_sublist(list1, list2):
    len1 = len(list1)

    # float list1 to match list2
    for i in range(len(list2) - len1+1):
        if list1 == list2[i:(len1+i)]:
            return True
    return False


"""
    split the whole traffic matrix into sub traffic matrix
    we have to consider the traverse flows
    whole_matrix: traffic matrix of the whole network
    groups_list: group list of the switches, each element of the 
                list is a node id list of the group
    whole_flow_dict: the flow_dict of the big network
    
    return: the Traffic matrix list of each group
"""
def split_matrix(whole_matrix, groups_list, whole_network):

    traffic_list = []
    for group in groups_list:
        matrix_size = len(whole_matrix)
        sub_matrix = np.zeros((matrix_size, matrix_size), dtype=np.float)

        # the source and destination all in group
        for i in group:
            for j in group:
                sub_matrix[i][j] = whole_matrix[i][j]

        for key_f, flow in whole_network.flows_dict.iteritems():

            if flow.src in group and flow.dst in group:
                continue
            path = whole_network.paths_dict[flow.cur_path_id]
            path_list = path.nodes
            if flow.src in group and flow.dst not in group:
                for i in range(len(path_list)):
                    if path_list[i] in group:
                        continue
                    else:
                        end_node = path_list[i-1]
                        sub_matrix[flow.src][end_node] += whole_matrix[flow.src][flow.dst]
                        break
            if flow.dst in group and flow.src not in group:
                for i in range(len(path_list)):
                    if path_list[i] in group:
                        sub_matrix[path_list[i]][flow.dst] += whole_matrix[flow.src][flow.dst]
                        break

            if flow.src not in group and flow.dst not in group:
                enter_node = -1
                end_node = -1
                enter_flag = False
                for i in range(len(path_list)):
                    if not enter_flag and path_list[i] in group:
                        enter_flag = True
                        enter_node = path_list[i]
                    if enter_flag and path_list[i] not in group:
                        end_node = path_list[i-1]

                    if enter_node != -1 and end_node != -1 and enter_flag:
                        sub_matrix[enter_node][end_node] += whole_matrix[flow.src][flow.dst]

        traffic_list.append(sub_matrix.tolist())

    return traffic_list


"""
    get the flows which contains ciritical links
    n: the Network object
    return: the flow list qualified.
"""
def get_critical_link_flows(n, critical_list):
    critical_link_flowsid_set = set()
    for f_k, f_v in n.flows_dict.iteritems():
        cur_path = n.paths_dict[f_v.cur_path_id]
        for l_i in cur_path.links:
            # onece one of the link of the flow is a
            # critical link add the flow to the set
            if l_i in critical_list:
                critical_link_flowsid_set.add(f_k)
                break
    return list(critical_link_flowsid_set)


"""
    get all the parameters required for further calculation
    net: the Net object
    return: serveral return values with the following sequence:
        nodes_num, links_num, total_paths_num, flows_num, p_l, p_n
"""
def get_params(net, g):
    nodes_num = len(net.nodes_dict)
    flows_num = len(net.flows_dict)

    total_paths_num = len(net.paths_dict)

    # generate the p_l matrix
    links_num = len(net.links_dict)

    # preprocess the final matrix
    p_l = []
    for i in range(0, total_paths_num):
        tmp = []
        for j in range(0, links_num):
            tmp.append(0)
        p_l.append(tmp)
    # set value to the final matrix
    for p_k, p_v in net.paths_dict.iteritems():
        for l_id in p_v.links:
            p_l[p_k][l_id] = 1

    # generate the p_n matrix
    nodes_num = len(net.nodes_dict)

    # preprocess the final matrix
    p_n = []
    for i in range(0, total_paths_num):
        tmp = []
        for j in range(0, nodes_num):
            tmp.append(0)
        p_n.append(tmp)

    # set values to the final matrix

    #get the new_id and renumbered id mapping
    mapping_table = cal_id_mapping(g)
    for p_k, p_v in net.paths_dict.iteritems():
        for n_id in p_v.nodes:
            n_id = mapping_table[int(n_id)]
            p_n[p_k][n_id] = 1

    return nodes_num, links_num, total_paths_num, flows_num, p_l, p_n


"""
    get path candidate for each flow
    n: the Network object
    return: a path candidate matrix which indicates the relationship of flows and paths.
"""
def get_path_candidate(n):
    pathcandidate = []
    for f_key, flow in n.flows_dict.iteritems():
        tmppaths = []
        for j in range(len(n.paths_dict)):
            if j in flow.path_list:
                tmppaths.append(1)
            else:
                tmppaths.append(0)
        pathcandidate.append(tmppaths)
    return pathcandidate

"""
    get path id list of each flow
    n: the Network Object
    return: the flow_path_id list
"""
def get_flow_path_id(n):
    res_list = []
    for f_id, flow in n.flows_dict.iteritems():
        res_list.append(flow.path_list)
    return res_list


"""
    calculate the map of old id and renumbered id
    
    g: the igraph object
    
    return: the mapping table
"""
def cal_id_mapping(g):
    id_mapping_table = dict()

    vs = VertexSeq(g)
    for v in vs:
        id_mapping_table[int(v['id'])] = v.index

    return id_mapping_table


"""
    get the old_y, old_y is the relationship matrix between flows and paths.
    network: the Net or SubNetwork object
    g: the igraph object

    return: old_y. note that the id of old y is renumbered.
"""
def get_old_y(network):

    oldy_shape = (len(network.flows_dict), len(network.paths_dict))
    old_y = np.zeros(oldy_shape, dtype=np.int)
    for flow_k, flow in network.flows_dict.iteritems():
        old_y[flow.flow_id][flow.cur_path_id] = 1
    return old_y.tolist()


"""
    get the rate of each flow
    n: the Net or SubNetwork object
    return: the flow_rate list
"""
def get_flow_rate(network):
    # initialize flow_rate vector
    flow_rate = [0 for i in range(len(network.flows_dict))]

    for f_k, f_v in network.flows_dict.iteritems():
        flow_rate[f_k] = f_v.rate
    return flow_rate


"""
    get all flow id of a network
    network: the Net or SubNetwork object
    return: all flow id list
"""
def get_all_flows(network):
    all_flow_list = [flow_id for flow_id, flow in network.flows_dict.iteritems()]
    return all_flow_list


"""
    get all link rate of a network
    network: the Net or SubNetwork object
    return: the link rate list
"""
def get_link_rate(network):
    # init the link_rate list
    link_rate_list = [0 for i in range(len(network.links_dict))]
    for link_id, link in network.links_dict.iteritems():
        link_rate_list[link_id] = link.rate
    return link_rate_list


"""
    generate random traffic matrix
    matrix_shape:
    
    return: traffic matrix
"""
def generate_traffic_matrix(shape, link_capacity, ratio):
    traffic_matrix = np.zeros(shape, np.float)
    for i in range(shape[0]):
        for j in range(shape[1]):
            traffic_matrix[i][j] = random.uniform(0, link_capacity * ratio)
    return traffic_matrix


""""
    save generated traffic
    filename: file name of the traffic file
    matrix_list: traffic matrix list
"""
def save_gen_traffic(filename, matrix_list):
    with open(filename, 'w') as f:
        for i in range(len(matrix_list)):
            flatten_matrix = np.asarray(matrix_list[i]).ravel()
            for j in flatten_matrix:
                f.write('%d ' % j)
            f.write('\n')

"""
    read genenerated traffic from file
    filename: file name of the traffic matrix
    
    return: the traffic matrices list
"""
# def read_gen_traffic(filename):
#     traffic_list = []
#     with open(filename, 'r') as f:
#         for line in f:
#             str_list = line.split(' ')
#             tmp = []
#