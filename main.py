from Util import *
from Entity import *

from Network import Net
from SubNetwork import SubNetwork

from OptimalPy import *
import copy
import os
import sys
import getopt




# Global Variables
# k selected path K
k = 20
# k selected path have m intersection links
m = 10

# increase factor for traffic
traffic_factor = 1
# the threshold ratio for starting load balancing algorithm
LB_factor = 1

# flow table capacity for each switch
TB = 1000

OL = 20000

no_loop_para = 0.00000001

group_num = 2

failed_controller_num = 1

# test flag, true for test
isWriteFile = True


# the controller control power
a = 500

# the percentage of controlling flows
ratio = 0.9

topo = "AttMpls"



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

    n = Net(g, k, m, TB, group_num, topo)
    group_num = len(n.nodes_dict) / 5


    # calculate the groups
    groups_list = cal_cluster_group(cal_distance_matrix(n), group_num, a, n)

    subnet_list = []
    for group in groups_list:
        group_vs = g.vs.select(group)
        sub_g = g.subgraph(group_vs)

        # layout = sub_g.layout("kk")
        # plot(sub_g, layout=layout)
        subnet = SubNetwork(sub_g, k, m, TB, 1, topo, n)
        subnet_list.append(subnet)

    for matrix in matrices_list[:1]:
        domain_matrices = split_matrix(matrix, groups_list, n)
        n.apply_traffic(matrix)
        print n.calc_link_utilization()

        # apply subnetwork traffic
        for i in range(len(subnet_list)):
            subnet_list[i].apply_traffic(domain_matrices[i])
            print subnet_list[i].calc_link_utilization()









if __name__ == '__main__':

    main()