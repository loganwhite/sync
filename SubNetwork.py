from Network import *
from test import test_print_flows


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

    def __init__(self, g, k, m, TB, group_num, topo, whole_network, name):

        Net.__init__(self, g, k, m, TB, group_num, topo, name)
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
                    self.inner_flow_dict[i].whole_flow = whole_flow
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
        # # add the connecting links' utilization, if splitting
        # # groups using the cutting edage
        # for node in group_node_list:
        #     for key, link in self.whole_network.links_dict.iteritems():
        #         # find the links that connect to another domain
        #         # this means that the src node is in the domain
        #         # and the dst node is not in the domain
        #         if link.src != node:
        #             continue
        #         if link.dst in group_node_list:
        #             continue
        #         linkutil_list.append(link.rate / float(link.capacity))

        # add the subnetwork links' utilization
        for l_k, l_v in self.links_dict.iteritems():
            linkutil_list.append((l_k, (float(l_v.rate) / float(l_v.capacity))))
        res = max(linkutil_list, key=lambda t: t[1])

        print("link util at link: %d\n" % res[0])
        test_print_flows(self, res[0])

        return res[1]


    """
        get the candidate nodes that connects the following domain.
        
        return: the candidate nodes list of all subflows
    """
    def get_candidate_nodes(self, groups_list):
        candidate_nodes = dict()
        group_node_list = [node.node_id
                           for key, node in self.nodes_dict.iteritems()]

        for flow_id, flow in self.inner_flow_dict.iteritems():
            if not flow.is_subflow:
                continue

            # get the next node
            path_id = flow.cur_path_id
            cur_path = self.paths_dict[path_id]

            #original path means that the path in the whole network
            original_path_id = flow.whole_flow.cur_path_id
            original_path = self.whole_network.paths_dict[original_path_id]
            last_node = cur_path.nodes[-1]

            # get next node
            if last_node != original_path.nodes[-1] and last_node in original_path.nodes:
                next_node_index = original_path.nodes.index(last_node) + 1
                next_node = original_path.nodes[next_node_index]

                # get the group of the next node (next group)
                next_group = []
                for group in groups_list:
                    if next_node in group:
                        next_group = group
                        break

                # get all the edge nodes of getting to the next group
                tmp_nodes = set()
                for link_id, link in self.whole_network.links_dict.iteritems():
                    if link.src in group_node_list and link.dst in next_group:
                        tmp_nodes.add(link.src)
                candidate_nodes[flow_id] = list(tmp_nodes)

        return candidate_nodes


    def apply_modification_newOp(self, tuple):
        """
        apply changes to the new op results.
        :param tuple: contains, old flow, new flow and new path.
        :return: no return
        """

        for item in tuple:
            old_flow_id = item[0]
            new_flow_id = item[1]
            new_path_id = item[2]
            old_flow = self.flows_dict[old_flow_id]
            old_inner_flow = self.inner_flow_dict[old_flow_id]
            new_flow = self.flows_dict[new_flow_id]
            new_inner_flow = self.inner_flow_dict[new_flow_id]

            new_flow.cur_path_id = new_path_id
            from main import traffic_tranfer
            traffic_tranfer(self, old_flow_id, new_flow.dst)











