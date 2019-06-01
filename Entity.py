from igraph import *
from Util import *

# for easy to use, the path set do not have a particular class 
# defining. we use a simple list to store it.
# We have a global dict[path_id]path that stores all the paths on the net


"""
    The node class, it has only one property 'node_id'
    which is globally consistent
"""
class Node:
    def __init__(self, node_id, flowtbl_capacity=0, longi=0, lati=0, flowtbl_used = 0):
        self.node_id = node_id
        self.flowtbl_capacity = flowtbl_capacity
        self.flowtbl_used = flowtbl_used
        self.longi = longi
        self.lati = lati

    """
        Determine if the node is feasible on a particular path
        path_id: the id of the path
        paths_dict: the paths dict that contains all the path.

        return: True if the node is feasible on the path
                False if the node is not feasible on the path
    """
    def is_feasible_node(self, path_id, paths_dict):
        p = paths_dict[path_id]
        if self.node_id == p.dst:
            return False
        else:
            return True

"""
    The Link class,
    link_id: the globally unified id
    src: the start node_id of the link
    dst: the end node_id of the link
    rate: the traffic in total on this link
    capacity: the total traffic can be applied on the link 
"""
class Link:
    def __init__(self, link_id, src, dst, dist = 0,
            rate = 0, capacity = 9920000):
        self.link_id = link_id
        self.src = src
        self.dst = dst
        self.rate = rate
        self.capacity = capacity
        self.dist = dist

"""
    Tha Path class,
    path_id: the globally unified id
    src: the source node_id
    dst: the destination node_id
    nodes: the node_id list of the path and the sequence is the node sequence on the path
    links: the link_id set of the path
    install: if flowentries have installed on this path
"""
class Path:
    def __init__(self, path_id, src, dst, nodes=[], 
            links=[], install=False, congest=False):
        self.path_id = path_id
        self.src = src
        self.dst = dst
        self.nodes = nodes
        self.links = links
        self.install = install
        self.congest = congest

    def hops(self):
        return len(self.links)

"""
    The Flow class
    flow_id: the unified id of flow
    src: the source node_id of the flow
    dst: the destination node_id of the flow
    rate: the total traffic on this flow
    path_list: the path_list list of this flow
    cur_path_id: the path_id of the Path that being used by the Flow
    inst_nodes: the node_id set of the current installed nodes
"""
class Flow:
    def __init__(self, flow_id, src, dst, rate=0, path_list=[],cur_path_id=0, inst_nodes=set(), distance=0):
        self.flow_id = flow_id
        self.src = src
        self.dst = dst
        self.rate = rate
        self.path_list = path_list
        self.cur_path_id = cur_path_id
        self.inst_nodes = inst_nodes
        self.min_dist = distance





    """
        Determine if the flow is feasible
        path_dict: the dictionary of all path with path_id as its key

        return: True if the flow is feasible
                False if the flow is not feasible
    """
    def is_feasible_flow(self, paths_dict):
        if len(self.path_list) < 2:
            return False
        
        for p_id in self.path_list:
            if paths_dict[p_id].hops() > 1:
                return True
        return False

    """
        Generate K paths in a flow which have m intersection links
        k: the number of paths
        m: the number of links that are the same
    """
    def get_k_path(self, paths_dict, links_dict, k, m):
        k_path_id = []

        if self.path_list <= 0 or self.path_list <= k:
            return self.path_list

        # get flow paths list
        flowpath_list = []
        for p_id in self.path_list:
            flowpath_list.append(paths_dict[p_id])

        count = 0
        for p in flowpath_list:
            # flag used for indicating the path are qualified to all other paths
            flag = 0
            if count >= k:
                break
            for q in flowpath_list:
                if p.path_id != q.path_id:
                    # if the path p is not qualified mark flag and go to the next one.
                    if not (len(set(p.links) & set(q.links)) <= m ):
                        flag = 1
                        break
            if not flag:
                k_path_id.append(p.path_id)
                count += 1
        if len(k_path_id) == 0:
            k_path_id.append(self.path_list[0])
        self.path_list = k_path_id


class InnerFlow(Flow):
    def __init__(self, flow_id, src, dst, rate=0, path_list=[], cur_path_id=0, inst_nodes=set(), distance=0, is_subflow=False):
        Flow.__init__(self, flow_id, src, dst, rate, path_list,cur_path_id, inst_nodes, distance)
        self.is_subflow = is_subflow
        self.whole_flow = None