from Network import *


class SubNetwork(Net):
    """
         construct the Net from a igraph object g, Then initialize it
         and generate the nodes_dict, links_dict, paths_dict and flows_dict.

         g: the igraph object
         k: the number of select paths in a flow
         m: the number of intersection link of the selected path in a flow
         TB: the flow table capacity of a switch
         group_num: the number of groups
     """

    def __init__(self, g, k, m, TB, group_num, topo, whole_network):

        Net.__init__(self, g, k, m, TB, group_num, topo)
        self.inner_flow_dict = dict()
        self.whole_network = whole_network

        for i in range(len(self.flows_dict)):
            flow = self.flows_dict[i]
            self.inner_flow_dict[i] = InnerFlow(flow.flow_id, flow.src, flow.dst, flow.rate,
                                                flow.path_list, flow.cur_path_id,
                                                flow.inst_nodes, flow.min_dist)
            # avoid the self to self
            if flow.src == flow.dst:
                continue

            # for each small flow, check all big flow to see if it is a sub flow
            for key_f, whole_flow in whole_network.flows_dict.iteritems():

                path = whole_network.paths_dict[whole_flow.cur_path_id]
                whole_path_list = path.nodes

                subflow_path_list = self.paths_dict[flow.cur_path_id].nodes
                if len(subflow_path_list) >= len(whole_path_list):
                    continue
                # get the sub network nodes list
                # and check if all node in whole path list
                # is a subset of the group nodes
                group_node_list = [node.node_id
                                   for key, node in self.nodes_dict.iteritems()]
                if set(whole_path_list).issubset(set(group_node_list)):
                    continue

                if is_sublist(subflow_path_list, whole_path_list):
                    self.inner_flow_dict[i].is_subflow = True
                    break

    """
        Override method
        calculate the subnetwork link utilization,
        include the links connecting to adjacent domains.
        
        return: the link utilization
    """
    def calc_link_utilization(self):
        group_node_list = [node.node_id
                                   for key, node in self.nodes_dict.iteritems()]

        linkutil_list = []
        # add the connecting links' utilization
        for node in group_node_list:
            for key, link in self.whole_network.links_dict.iteritems():
                # find the links that connect to another domain
                # this means that the src node is in the domain
                # and the dst node is not in the domain
                if link.src != node:
                    continue
                if link.dst in group_node_list:
                    continue
                linkutil_list.append(link.rate / float(link.capacity))

        # add the subnetwork links' utilization
        for l_k, l_v in self.links_dict.iteritems():
            linkutil_list.append(float(l_v.rate) / float(l_v.capacity))

        return max(linkutil_list)







