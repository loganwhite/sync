from Network import *
from SubNetwork import *
from Util import *


def test_print_all_link_above_threshold(network, threshold):
    for link_id, link in network.links_dict.iteritems():
        if link.rate > (threshold * link.capacity):
            print("%d\t %f\n" % (link_id, link.rate))


def test_print_flows(network, link_id):
    '''
    print flows id of a given link_id
    :param network:
    :param link_id:
    :return:
    '''
    for flow_id, flow in network.flows_dict.iteritems():
        path = network.paths_dict[flow.cur_path_id]
        if link_id in path.links:
            print("%d " % flow_id)


