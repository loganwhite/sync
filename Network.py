from os import path

from igraph import *
from Util import *
from Entity import *

import math
import numpy as np


"""
    The Net class,
    It has the following member variables
    nodes_dict: the dictionary contains all the nodes of the Net
    links_dict: the dictionary contains all the links of the Net
    paths_dict: the dictionary contains all the paths of the Net
    flows_dict: the dictionary contains all the flows of the Net
    k: the number of select paths in a flow
    m: the number of intersection link of the selected path in a flow
"""
class Net:

    """
        construct the Net from a igraph object g, Then initialize it 
        and generate the nodes_dict, links_dict, paths_dict and flows_dict.

        g: the igraph object
        k: the number of select paths in a flow
        m: the number of intersection link of the selected path in a flow
        TB: the flow table capacity of a switch
        group_num: the number of groups
    """
    def __init__(self, g, k, m, TB, group_num, topo, name):
        self.name = self.__class__.__name__ + topo + name
        self.k = k
        self.m = m
        self.nodes_dict = dict()
        self.links_dict = dict()
        self.paths_dict = dict()
        self.flows_dict = dict()
        # used for indexing from (src, dst) tuple to the corresponding flow id
        self.flowID_dict = dict()
        self.link_weight_dict = dict() # key (src, dst) value weight
        self.linkID_dict = dict()   # key(src, dst) value id
        self.group_list = []
        self.group_num = group_num              # the number of groups
        self.topo = topo


        # get all nodes id from g and store Nodes into the nodes_dict
        vs = VertexSeq(g)
        for v in vs:
            node_id = int(v["id"])
            lati = float(v['Latitude'])
            longi = float(v['Longitude'])
            self.nodes_dict[node_id] = Node(node_id, lati=lati, longi=longi, flowtbl_used=TB)

        # print("in network number of nodes", len(self.nodes_dict))

        # get all links id from g and store Links into the links_dict
        es = EdgeSeq(g)
        link_id = 0
        tmp_edge_set = set()
        for e in es:
            # i = int(e.tuple[0])
            # j = int(e.tuple[1])
            i = int(e.source)
            j = int(e.target)

            i = int(g.vs[i]['id'])
            j = int(g.vs[j]['id'])
            tmp_edge_set.add((i, j, 1))
            # tmp_edge_set.add((i,j,e["weight"]))
        # print("in network, tmp_edge_set", tmp_edge_set)
        for e in tmp_edge_set:
            # generate the bidirectional link
            for i in range(2):

                # s = (self.nodes_dict[e[i % 2]].longi - self.nodes_dict[e[(i+1) % 2]].longi)**2 + (self.nodes_dict[e[i % 2]].lati - self.nodes_dict[e[(i + 1) % 2]].lati) ** 2
                # dist = math.sqrt( s )

                dist = haversine(self.nodes_dict[e[(i+1) % 2]].longi,
                                 self.nodes_dict[e[(i+1) % 2]].lati,
                                 self.nodes_dict[e[i % 2]].longi,
                                 self.nodes_dict[e[i % 2]].lati)

                link = Link(link_id, e[i % 2], e[(i+1) % 2], dist=dist)
                self.linkID_dict[(e[i % 2], e[(i+1) % 2])] = link_id
                self.link_weight_dict[(e[i % 2],e[(i+1) % 2])] = e[2]
                if (e[0] == 1 and e[1] == 5) or (e[0] == 5 and e[1] == 1):
                    link.capacity = 2480000
                self.links_dict[link_id] = link
                link_id += 1
        
        
        # print("in network number of links", len(self.links_dict))
        #
        # get all the paths from g and store paths into the paths_dict
        # if path.exists('paths.log'):
        #     find_all_paths(self, g, self.link_weight_dict)
        # else:
        #     find_all_paths_to_file(self, g, self.link_weight_dict)
        if path.exists(self.name):
            find_all_paths(self, g)
        else:
            find_all_paths_to_file(self, g, self.name)

        # generate all the flows
        gen_flow_all(self, k, m)


        self.group_list = group_vertics(g, self.group_num)
        # gen_area_flow_all(self, self.group_list)

        
    
    """
        Apply traffic matrix from 'matrix' to both flow and path

        matrix: the traffic matrix
    """
    def apply_traffic(self, matrix):
        n = len(matrix)
        # apply traffic to all flows
        for i in range(0, n):
            for j in range(0, n):
                if (i, j) not in self.flowID_dict:
                    continue
                flow_id = self.flowID_dict[(i, j)]
                flow = self.flows_dict[flow_id]
                flow.rate = matrix[i][j]
                p_id = flow.cur_path_id
                # apply traffic to path
                path = self.paths_dict[p_id]
                for l_id in path.links:
                    link = self.links_dict[l_id]
                    # since different paths may use the same link
                    link.rate += flow.rate
                    # judge if the path is congested
                    if link.rate > link.capacity:
                        path.congest = True
                        
        
        #print congestion paths
        # for p_k, p_v in self.paths_dict.iteritems():
        #     if p_v.congest:
        #         print p_k
        # input()

    """
        Calculate the link utilization of the network. Link utilization is the
        maximum rate on a link over the link capacity.

        return: the link utilization
    """
    def calc_link_utilization(self):
        linkutil_list = []

        for l_k, l_v in self.links_dict.iteritems():
            linkutil_list.append(float(l_v.rate) / float(l_v.capacity))
        
        return max(linkutil_list)

    """
        Calculate the number of entries modified

        return: the total number of entry changes on the network
    """
    def calc_entry_overhead(self):
        total_overhead = 0

        for i in range(len(self.flows_dict)):
           total_overhead += len(self.flows_dict[i].inst_nodes)
        
        return total_overhead

    """
        Get the maximum link load of the network

        return: The maximum load rate of the network
    """
    def get_max_load(self):
        linkrate_list = []

        for l_k, l_v in self.links_dict.iteritems():
            linkrate_list.append(l_v.rate)
        
        return max(linkrate_list)


    """
        Change path for a flow based on the calculation

        tuples: tuple list with (flow_id, path_id, value) format

    """
    def apply_modification(self, tuples, old_y, new_y):
        
        for item in tuples:
            flow = self.flows_dict[item[0]]
            if flow.cur_path_id != item[1]:
                path_old = self.paths_dict[flow.cur_path_id]
                path_new = self.paths_dict[item[1]]
                for l in path_old.links:
                    self.links_dict[l].rate -= flow.rate
                for l in path_new.links:
                    self.links_dict[l].rate += flow.rate
                    

        for tpl in tuples:
            flow_id = tpl[0]
            path_id = tpl[1]
            self.flows_dict[flow_id].cur_path_id = path_id
            # print("result",self.flows_dict[flow_id].src, self.flows_dict[flow_id].dst, self.paths_dict[path_id].nodes)

        # self.update_node_flowentry(old_y, tuples)

    """
        update flowentry useage
    """
    def update_node_flowentry(self, old_y, tpl):
        # find the changed flows
        changed_flow_id_list = []
        for t in tpl:
            changed_flow_id_list.append(t[0])

        for f_k in changed_flow_id_list:

            f_v = self.flows_dict[f_k]
            cur_path = self.paths_dict[f_v.cur_path_id]

            # get the old path
            oldpath_id = 0
            for j in range(len(old_y[f_k])):
                if old_y[f_k][j] == 1:
                    oldpath_id = j
            old_path = self.paths_dict[oldpath_id]
            
            # for each node, check if the rest of the road from this node is a shortest path
            # since the first path of each flow is the shortest path we can make a compare 
            # from this one to the one of the same src and dst flow.

            inst_nodes = []

            # do not get to the final element
            stored_index = 0
            # since the old_path is shorter.
            for i in range(0, len(old_path.nodes) - 1):
                stored_index = i
                

                # find the difference stop compare this road
                # try to find if this node to the destination
                # has another shortest paths.
                if cur_path.nodes[i] != old_path.nodes[i]:
                    inst_nodes.append(cur_path.nodes[i-1])
                    break
            # try to find if this node to the destination is a shortest path
            for i in range(stored_index, len(cur_path.nodes) - 1):                
                
                # find the short path of current node to dst
                tmp_from = cur_path.nodes[i]
                tmp_to = f_v.dst

                flow = self.flows_dict[self.flowID_dict[(tmp_from, tmp_to)]]

                # make comparasion
                if cur_path.nodes[i:] != self.paths_dict[flow.path_list[0]].nodes:
                    inst_nodes.append(cur_path.nodes[i])
                else:
                    break
            f_v.inst_nodes = inst_nodes
            
            # modify flow entry number on nodes
            for n_id in f_v.inst_nodes:
                self.nodes_dict[n_id].flowtbl_used += 1
            

    """
        Fall back to shortest path while reaches the 5 minute timeout.
        restore the cur_path to shortest path and remove all the flow entries of a node
        remove all the rates of a link
    """
    def fall_back_shortest_path(self):
        # set the flow path to shortest path remove the installed flow entry node list
        for f_k, f_v in self.flows_dict.iteritems():
            f_v.cur_path_id = f_v.path_list[0]
            f_v.inst_nodes = []
        
        # remove the flow entries of each node
        for n_k, n_v in self.nodes_dict.iteritems():
            n_v.flowtbl_used = 0
        
        # remove the rate of each link
        for l_k, l_v in self.links_dict.iteritems():
            l_v.rate = 0
        
        # remove the properties on paths
        for p_k, p_v in self.paths_dict.iteritems():
            p_v.install = False
            p_v.congest = False


    """
        Calculate the multi-controller sychronization overhead
        tpls: the tuple list of changed flow and path

        return: the flow_id and sync overhead of changed flows
    """
    def mul_ctl_sync_overload(self, tpls):
        res_list = []
        changed_flow_id = []
        for item in tpls:
            changed_flow_id.append(item[0])
        
        for f_k in changed_flow_id:
            overhead = 0
            f_v = self.flows_dict[f_k]
            path = self.paths_dict[f_v.cur_path_id]
            groupuse_dict = dict()
            for n in path.nodes:
                for i in range(self.group_num):
                    if n in self.group_list[i]:
                        groupuse_dict[i] = 1
                        continue
            
            # calculate sync overhead for a single flow
            ctl_used = 0
            for k, v in groupuse_dict.iteritems():
                if v == 1:
                    ctl_used += 1
            overhead += (ctl_used - 1)
            res_list.append((f_k, overhead))
        return res_list


    """
        get pair distance
        
        return: the matrix of pair
    """
    def pair_distance(self):
        dist = []
        for i in range(len(self.nodes_dict)):
            tmp = []
            for j in range(len(self.nodes_dict)):
                if (i, j) not in self.flowID_dict:
                    tmp.append(0)
                    continue
                flow_id = self.flowID_dict[(i, j)]
                flow = self.flows_dict[flow_id]

                # use time as distance
                tmp.append(flow.min_dist / 200000000)
            dist.append(tmp)

        return dist


    """
        Calculate the matrix of switch and flow relationship 
        
        return: the matrix of switch and flow relationship
    """
    def switch_flow_matrix(self):
        switch_flow = []

        for flow_id in range(len(self.flows_dict)):
            flow = self.flows_dict[flow_id]
            path = self.paths_dict[flow.cur_path_id]
            switch = []
            for i in range(len(self.nodes_dict)):
                if i in path.nodes:
                    switch.append(1)
                else:
                    switch.append(0)
            switch_flow.append(switch)

        return switch_flow

    """
        Calculate the matrix of switch and flow relationship, no last switch in the flow

        return: the matrix of switch and flow relationship
    """

    def switch_flow_nolast_matrix(self):
        switch_flow = []

        for flow_id in range(len(self.flows_dict)):
            flow = self.flows_dict[flow_id]
            path = self.paths_dict[flow.cur_path_id]
            switch = []
            for i in range(len(self.nodes_dict)):
                if i in path.nodes[:-1]:
                    switch.append(1)
                else:
                    switch.append(0)
            switch_flow.append(switch)

        return switch_flow


    """
        calculate the controller locations relationship list
        g: the igraph object
        num: the number of groups
        
        return: the list of controller locations relationship
    """
    def controll_location(self, g, num, ability):

        # if len(self.nodes_dict) == 25:
        #     groups_list = [[0, 1, 7], [ 12,21, 22], [20, 8,9], [2, 18, 24], [19, 17], [16,5], [4, 6, 14],[15, 10 ,11], [16], [13,23]]
        # elif len(self.nodes_dict) == 12:
        #     groups_list = [[9, 0, 10, 8, 11], [1, 7, 2, 3, 4], [6, 5]]
        # else:
        #     groups_list = group_vertics(g, num)

        # groups_list = group_vertics(g, num)

        groups_list = cal_cluster_group(cal_distance_matrix(self), num, ability, self)
        self.group_list = groups_list

        location_node_id = find_central_vertex_groups(g, groups_list)

        loc_list = []
        for i in range(len(self.nodes_dict)):
            if i in location_node_id:
                loc_list.append(1)
            else:
                loc_list.append(0)

        return loc_list

    """
        calculate the flow number of each switch
        switch_id: the id of switch
        
        return: the number of flows of the switch
    """
    def switch_flows(self, switch_id):
        np_flow_swith = np.asarray(self.switch_flow_matrix())
        np_switch_flow = np_flow_swith.transpose()
        switch_flow = np_switch_flow.tolist()

        return sum(switch_flow[switch_id])


    def get_flow_link_utilization(self, flow_id):
        """
        get flow link utilization of flow_id. Flow link utilization is the
        maximum link utilization of current path links.
        :param flow_id: flow ID
        :return: flow link utilization
        """
        flow = self.flows_dict[flow_id]
        path = self.paths_dict[flow.cur_path_id]

        max_util = 0
        for l_id in path.links:
            tmp_util = self.links_dict[l_id].rate / float(self.links_dict[l_id].capacity)
            if tmp_util > max_util:
                max_util  = tmp_util
        return max_util

        

            



        

