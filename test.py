from Network import *
from SubNetwork import *
from Util import *


def test_print_all_link_above_threshold(network, threshold):
    for link_id, link in network.links_dict.iteritems():
        if link.rate > (threshold * link.capacity):
            print("%d\t %f\n" % (link_id, link.rate))



