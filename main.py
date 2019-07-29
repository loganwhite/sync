from Placement import Placement
from Util import *
from Entity import *

from Network import Net
from SubNetwork import SubNetwork

from OptimalPy import *
from OptimalPy_new import *
import copy
import os
import sys
import getopt

from Settings import *      # global variables

from test import *          # test functions






def main():
    # declare the global variables
    global a, ratio, group_num, topo
     # attempt to get the arguments.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:r:t", ["a=", "ratio=", "topo="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        print "a:r:t: a= ratio= topo="
        sys.exit(2)

    for o, value in opts:
        if o in ('-a', "--a"):
            a = int(value)
        elif o in ("-r", "--ratio"):
            ratio = float(value)
        # elif o in ('-g', "--group-num"):
        #     group_num = int(value)
        elif o in ('-t', "--topo"):
            topo = value
        else:
            assert False, "unhandled option"


    file_prefix = 'data/a_' + topo + str(a) + 'r_' + str(ratio)

    # initialization read traffic matrix and generate the graph
    # from gml file and construct the experiemntal network
    matrices_list = read_traffic("X01", traffic_factor)
    g = Graph.Read_GML(topo + ".gml")

    # layout = g.layout("kk")
    # plot(g, layout=layout)

    n = Net(g, k, m, TB, group_num, topo, "whole")

    control_loc = n.controll_location(g, group_num, a)
    place = Placement(n.pair_distance(), len(n.flows_dict), len(n.nodes_dict), control_loc)
    place_nodes = [i for i in range(len(n.nodes_dict))]
    place_ability = [a for i in range(len(n.nodes_dict))]
    place.process(n.switch_flow_matrix(), place_nodes,
                  place_nodes, place_ability, ratio,
                  len(n.flows_dict))
    place_z = round_matrix(place.z)

    group_num = len(n.nodes_dict) / 5


    # calculate the groups
    # groups_list = cal_cluster_group(cal_distance_matrix(n), group_num, a, n)
    groups_list = get_group_list_from_switch_contro(place_z)
    groups_list = adjust_groups(groups_list, n)
    subnet_list, subgraph_list = cal_subnets(g, groups_list, n)



    for matrix in matrices_list[:1]:
        # used for att network
        node_num = len(n.nodes_dict)
        matrix = generate_traffic_matrix((node_num, node_num), link_capacity, traffic_gen_ratio)

        domain_matrices = split_matrix(matrix, groups_list, n)
        n.apply_traffic(matrix)
        print n.calc_link_utilization()

        # critical_list_whole = get_all_links(n)
        critical_link_list_whole = get_critical_link(n, threshold)
        critical_flow_whole = get_critical_link_flows(n, critical_link_list_whole)
        LB = get_link_capacity(n)
        pathcandidate = get_path_candidate(n)
        flow_pathid_list = get_flow_path_id(n)
        # op_whole = init_op(n, pathcandidate, flow_pathid_list, LB, g)
        oldy_whole = get_old_y(n)
        flows_rate_whole = get_flow_rate(n)
        all_flow_id_whole = get_all_flows(n)
        link_rate_whole = get_link_rate(n)

        # # whole network optimization
        # tpls_whole, new_y_whole = op_whole.process(oldy_whole, flows_rate_whole,
        #                                            link_rate_whole, critical_flow_whole)
        # n.apply_modification(tpls_whole, oldy_whole, new_y_whole)
        #
        # print n.calc_link_utilization()
        # print '\n'

        critical_list_subs = []
        critical_flow_subs = []
        sub_LBs = []
        sub_pathcandidate = []
        sub_flow_pathid_list = []
        sub_ops = []
        sub_oldys = []
        sub_flows_rates = []
        sub_all_flow_ids = []
        sub_link_rates = []
        sub_tpls = []
        sub_new_y = []
        for i in range(len(subnet_list)):
            # apply subnetwork traffic
            subnet_list[i].apply_traffic(domain_matrices[i])
            prev_util = subnet_list[i].calc_link_utilization()

            # calculate the critical link and flow
            critical_list_subs.append(get_critical_link(subnet_list[i], threshold))
            critical_flow_subs.append(get_critical_link_flows(subnet_list[i],
                                                              critical_list_subs[i]))
            sub_LBs.append(get_link_capacity(subnet_list[i]))
            sub_pathcandidate.append(get_path_candidate(subnet_list[i]))
            sub_flow_pathid_list.append(get_flow_path_id(subnet_list[i]))
            sub_ops.append(init_op(subnet_list[i], sub_pathcandidate[i],
                                   sub_flow_pathid_list[i], sub_LBs[i], subgraph_list[i]))
            sub_oldys.append(get_old_y(subnet_list[i]))
            sub_flows_rates.append(get_flow_rate(subnet_list[i]))
            sub_all_flow_ids.append(get_all_flows(subnet_list[i]))
            sub_link_rates.append(get_link_rate(subnet_list[i]))

            if prev_util <= threshold:
                print("subnetwork %d already satisfied the link util criteria\n" % i)
                continue
            print("showing util before op: %f" % prev_util)

            print("start showing link util before")
            test_print_all_link_above_threshold(subnet_list[i], threshold)

            tmp_tpls, tmp_new_y = sub_ops[i].process(sub_oldys[i], sub_flows_rates[i],
                                                    sub_link_rates[i], critical_flow_subs[i])

            # for flow_id, flow in subnet_list[i].inner_flow_dict.iteritems():
            #     print("%d\t%d\n" %(flow_id, flow.cur_path_id))

            sub_tpls.append(tmp_tpls)
            sub_new_y.append(tmp_new_y)
            subnet_list[i].apply_modification(tmp_tpls, sub_oldys[i], tmp_new_y)
            tmp_util = subnet_list[i].calc_link_utilization()
            # print("start showing link util after")
            # test_print_all_link_above_threshold(subnet_list[i], threshold)

            print "//////////////////////////////////////"
            print("after 1st op and Before select new node %f\n" % tmp_util)


            # if exceeds threshold
            if prev_util <= threshold:
                continue

            # adjust with current subnet src and dst
            tmp_tpls, tmp_new_y = sub_ops[i].process(sub_oldys[i],
                                                     sub_flows_rates[i],
                                                     sub_link_rates[i],
                                                     critical_flow_subs[i])

            sub_tpls.append(tmp_tpls)
            sub_new_y.append(tmp_new_y)
            subnet_list[i].apply_modification(tmp_tpls, sub_oldys[i], tmp_new_y)

            new_tmp_util = subnet_list[i].calc_link_utilization()
            print("1st reroute linkutil %f of subnetwork %d\n" % (new_tmp_util, i))

            # change the dst until satisfy the link util requirement
            if new_tmp_util <= threshold:
                continue


            print("start changing dst process on subnetwork %d\n" % i)
            candidate_nodes = subnet_list[i].get_candidate_nodes(groups_list)

            # sort the flow according to the link utilization, desc
            sorted_flows = get_sorted_reroute_flows(candidate_nodes, subnet_list[i])
            sorted_flowsid = [item[0] for item in sorted_flows]

            sub_newOp = init_newOp(subnet_list[i], sub_pathcandidate[i],
                                   sub_flow_pathid_list[i], sub_LBs[i],
                                    subgraph_list[i], candidate_nodes)
            newOp_oldy = get_newOp_oldy(subnet_list[i])
            flow_rate = get_flow_rate(subnet_list[i])
            link_rate = get_link_rate(subnet_list[i])

            sub_newOp.process(newOp_oldy, flow_rate, link_rate, sorted_flowsid)




            # a copy of current best network condition (lowest link util)
            best_subnet = copy.deepcopy(subnet_list[i])
            for flow_id, candidate_dst in candidate_nodes.iteritems():
                cur_subflow = subnet_list[i].inner_flow_dict[flow_id]

                # this is absolutely a subflow, because candidate
                # is contains only subflows.
                if not cur_subflow.is_subflow:
                    continue

                # remove the current dst node in the candidate list
                if cur_subflow.dst in candidate_dst:
                    candidate_dst.remove(cur_subflow.dst)

                # test flag
                flag = 0
                for node in candidate_dst:
                    if node == subnet_list[i].inner_flow_dict[flow_id].src:
                        continue
                    traffic_tranfer(subnet_list[i], flow_id, node)
                    tmp_tpls, tmp_new_y = sub_ops[i].process(sub_oldys[i], sub_flows_rates[i],
                                                             sub_link_rates[i], critical_flow_subs[i])
                    sub_tpls.append(tmp_tpls)
                    sub_new_y.append(tmp_new_y)
                    subnet_list[i].apply_modification(tmp_tpls, sub_oldys[i], tmp_new_y)
                    new_tmp_util = subnet_list[i].calc_link_utilization()

                    print("current link util of subnetwork %d is: %f\n" % (i, new_tmp_util))

                    # if this dst cannot be the current best
                    if new_tmp_util >= best_subnet.calc_link_utilization():
                        continue

                    if new_tmp_util <= threshold:
                        print "find a suitable dst node\n"
                        flag = 1
                        subnet_list[i].migrate_next_grp_traffic()
                        break

                if flag == 1:
                    break
            print("new subnetwork %d util: %f\n" % (i, subnet_list[i].calc_link_utilization()))















"""
    Calculate the SubNetwork objects
    
    g: the whole network igraph object
    groups_list: the list of node groups of subnetwork
    n: the whole network Net object
    
    return: subnet_list: the list of SubNetwork objects
"""
def cal_subnets(g, groups_list, n):
    subnet_list = []
    subgraph_list = []
    for group in groups_list:
        group_vs = g.vs.select(group)
        sub_g = g.subgraph(group_vs)
        subgraph_list.append(sub_g)

        # layout = sub_g.layout("kk")
        # plot(sub_g, layout=layout)
        subnet = SubNetwork(sub_g, k, m, TB, 1, topo, n, ''.join(str(e) for e in group))
        subnet_list.append(subnet)
    return subnet_list, subgraph_list

"""
    Get all links' id
    
    network: the Net or SubNetwork object
    
    return: the list of all links in network
"""
def get_all_links(network):
    all_links = []

    for key, value in network.links_dict.iteritems():
        all_links.append(key)

    return all_links


"""
    Get critical links' id

    network: the Net or SubNetwork object
    threshold: the threshold of the link utilization.

    return: the list of critical links in network
"""
def get_critical_link(network, threshold):
    critical_link = []
    for key, value in network.links_dict.iteritems():
        if value.rate > (threshold * value.capacity):
            critical_link.append(key)

    return critical_link


"""
    Get link capacity list
    
    network: the Net or SubNetwork object
    
    return: capacity list
"""
def get_link_capacity(network):
    LB = []
    for i in range(0, len(network.links_dict)):
        LB.append(network.links_dict[i].capacity * LB_factor)
    return LB


"""
    init Op algorithm
    
    network: the Net or SubNetwork object
    
    return Optimal object
"""
def init_op(network, pathcandidate, flow_pathid_list, LB, g):
    nodes_num, links_num, total_paths_num, flows_num, p_l, p_n = get_params(network, g)
    op = Optimal(total_paths_num, flows_num, links_num, nodes_num,
                 p_l, p_n, LB, TB, OL, pathcandidate,
                 flow_pathid_list, no_loop_para)

    return op

def init_newOp(network, pathcandidate, flow_pathid_list, LB, g, flow_candidate_dict):
    """
    init the new Op object
    :param network:
    :param pathcandidate:
    :param flow_pathid_list:
    :param LB:
    :param g:
    :param flow_candidate_dict:
    :return:
    """
    nodes_num, links_num, total_paths_num, flows_num, p_l, p_n = get_params(network, g)

    # calculate the flow-flow-pathcandidate  3d matrix
    flow_flowcandidate_path = calculate_flow_flow_path_matrix(flow_candidate_dict, network)

    new_op = Optimal_new(total_paths_num, flows_num,
                         links_num, nodes_num, p_l, p_n,
                         LB, TB, OL, pathcandidate,
                         flow_pathid_list, no_loop_para,
                         flow_flowcandidate_path)
    return new_op


"""
    remove flow A traffic to flow B
    
    flow_id: the id of flow A
    new_dst: the dst of flow B
    network: the SubNetwork object    
"""
def traffic_tranfer(network, flow_id, new_dst):
    flow = network.flows_dict[flow_id]

    # remove the rate on old flow, and links
    rate = flow.rate
    flow.rate = 0
    network.inner_flow_dict[flow_id].rate = 0
    path = network.paths_dict[flow.cur_path_id]
    for link_id in path.links:
        network.links_dict[link_id].rate -= rate

    # apply traffic on new flow
    # get the new flow id
    new_flow_id = network.flowID_dict[(flow.src, new_dst)]
    network.inner_flow_dict[new_flow_id].rate += rate
    network.flows_dict[new_flow_id].rate += rate
    path = network.paths_dict[network.inner_flow_dict[new_flow_id].cur_path_id]
    for link_id in path.links:
        network.links_dict[link_id].rate += rate



def get_group_list_from_switch_contro(switch_contro):
    """
    get group list from switch controller relationship
    :param switch_contro: the switch controller relationship matrix
    :return: group list
    """
    contro_switch = matrix_transpose(switch_contro)

    group_list = []
    for item in contro_switch:
        if sum(item) != 0:
            tmp = []
            for j in range(len(item)):
                if item[j] == 1:
                    tmp.append(j)
            group_list.append(tmp)

    return group_list

def adjust_groups(groups_list, whole_network):
    """
    adjust the groups and make them connected by nodes, not by edge
    which means that the cut node is in either of the groups connected.
    :param groups_list: the node id list of the separated groups
    :param whole_network:
    :return: a new groups_list
    """
    num_node = len(whole_network.nodes_dict)
    visited = np.zeros((num_node, num_node), dtype=np.int)

    new_grps_list = []

    for i in range(len(groups_list)):
        # find connecting edge between anyother groups
        cur_grp = groups_list[i]
        new_grp = copy.deepcopy(cur_grp)   # make a deepcopy in case of it is a reference
        for j in range(len(groups_list)):
            if i == j:
                continue
            cmp_grp = groups_list[j]

            # loop the elements in the current group
            for cur_elem in cur_grp:
                for cmp_elem in cmp_grp:
                    if (cur_elem, cmp_elem) in whole_network.linkID_dict and\
                            not visited[cur_elem][cmp_elem] and not visited[cmp_elem, cur_elem]:
                        # if the elem has already been taken
                        if cmp_elem not in new_grp:
                            new_grp.append(cmp_elem)
                        # tag the link has been processed
                        visited[cur_elem][cmp_elem] = visited[cmp_elem][cur_elem] = 1

        new_grps_list.append(new_grp)
    return new_grps_list


def get_sorted_reroute_flows(candidate_nodes, network):
    """
    get the list of sorted flow id
    :param candidate_nodes: the calculated candidate nodes.
    :param network: the network object
    :return: the list of sorted flow id
    """
    flow_linkutil_tuple_list = []

    # get flow IDs
    for flow_id, _ in candidate_nodes.iteritems():
        flow_link_util = network.get_flow_link_utilization(flow_id)
        flow_linkutil_tuple_list.append((flow_id, flow_link_util))

    sorted(flow_linkutil_tuple_list, key=lambda t: t[1], reverse=True)

    return flow_linkutil_tuple_list



def calculate_flow_flow_path_matrix(flow_candidate, network):
    """
    get the flow-flowcandidate-candidateflowpath matrix (3D)
    :param flow_candidate: flow_candidate dict
    :param network: the network object
    :return: the 3D matrix
    """
    flows_num = len(network.flows_dict)
    path_num = len(network.paths_dict)
    flow_flowcandidate_path = np.zeros((flows_num, flows_num, path_num))
    for flow_id, candidate_dst in flow_candidate.iteritems():

        # add the flow itself as a flow candidate
        for path_id in network.flows_dict[flow_id].path_list:
            flow_flowcandidate_path[flow_id][flow_id][path_id] = 1
        src = network.flows_dict[flow_id].src
        for dst in candidate_dst:
            if (src, dst) in network.flowID_dict:
                candidate_flow_id = network.flowID_dict[(src, dst)]
                candidate_flow = network.flows_dict[candidate_flow_id]
                for path_id in candidate_flow.path_list:
                    flow_flowcandidate_path[flow_id, candidate_flow_id, path_id] = 1
    return flow_flowcandidate_path









if __name__ == '__main__':

    main()