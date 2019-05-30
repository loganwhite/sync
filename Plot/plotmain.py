from Plot import *
from Util import *
from Network import *
from PlotUtil import *




def main():
    algname_index_dict = {}
    algname_lagend_dict = {'GreedyAlg': 'RetroFlow',
                           'LpRecover': 'MappingLP',
                           'SwitchLP': 'SwitchLP',
                           'near': 'Nearest',
                           'opbound': 'AllFlowOptimal',
                           'recover': 'Optimal',
                           'weightbased': 'FlowNumGreedy',
                           'norm': 'Normal'}

    # ratio_list = sorted([0.8, 0.85, 0.9, 0.95, 1.0], reverse=True)

    ratio_list = sorted([0.9, 0.95, 1.0], reverse=True)
    topo_list = ['AttMpls']

    # ability_list = [500, 550, 600, 700, 800, 900, 1000]
    ability_list = [500]

    for ability in ability_list:
        source_file_prefix = 'data'+ os.sep+ 'a_' + str(ability) + os.sep
        topo_plot(ability, topo_list, ratio_list, source_file_prefix, algname_lagend_dict, algname_index_dict)





def topo_plot(ability, topo_list, ratio_list, source_file_prefix, algname_lagend_dict, algname_index_dict):
    for topo in topo_list:
        w = read_w('data/w_'+ topo)

        norm_filename = source_file_prefix + (topo + os.sep) + \
                         'norm' + os.sep + '.txt'

        norm_orig_x, norm_x, norm_contro_swtich, norm_failed_switch_loc, norm_flow_switch = read_data(norm_filename)
        norm_obj = cal_object(norm_contro_swtich, w)
        norm_control_flow_list = cal_control_flownum(norm_contro_swtich, norm_flow_switch)
        norm_switch_num_list = cal_control_switch_num(norm_contro_swtich)

        # processing
        norm_flows_list = []
        for item in norm_control_flow_list:
            norm_flows_list.append(len(item[1]))


        norm_switchs_list = []
        for item in norm_switch_num_list:
            norm_switchs_list.append(item[1])
        # end of processing

        for ratio in ratio_list:

            algfnames = [fname for fname in os.listdir(source_file_prefix + (topo + os.sep) +
                        ('r_' + str(ratio) + os.sep)) if ( 'norm' not in fname) or
                         ('weight' not in fname) or ('opbound') not in fname]
            for item in algfnames:
                if ('norm' in item):
                    algfnames.remove(item)
                    break

            for item in algfnames:
                if ('weightbased' in item):
                    algfnames.remove(item)
                    break

            for item in algfnames:
                if ('opbound' in item):
                    algfnames.remove(item)
                    break

            for item in algfnames:
                if ('LpRecover' in item):
                    algfnames.remove(item)
                    break

            for item in algfnames:
                if ('SwitchLP' in item):
                    algfnames.remove(item)
                    break

            algfnames.sort()

            alg_obj_one_list = []
            alg_obj_two_list = []
            alg_recflow_percen_one_list = []
            alg_recflow_percen_two_list = []
            alg_recswitchnum_one_list = []
            alg_recswitchnum_two_list = []

            alg_combi_contro_flow_num_one = []
            alg_combi_contro_flow_num_two = []




            # for each ratio, many algs, each alg a box, containing the number of flows of each controllers.
            ratio_alg_flownum_one_dict = dict()
            ratio_alg_flownum_two_dict = dict()
            ratio_alg_switchNum_one_dict = dict()
            ratio_alg_switchNum_two_dict = dict()


            alg_count = 0
            algfnames.sort()
            for alg in algfnames:

                if 'norm' in alg:
                    continue

                ratio_object_one_list = []
                ratio_recflow_percen_one_list = []
                ratio_recswitchnum_one_list = []
                ratio_controflownum_one_list = []

                ratio_object_two_list = []
                ratio_recflow_percen_two_list = []
                ratio_recswitchnum_two_list = []
                ratio_controflownum_two_list = []

                combi_count = 0
                combifname = [fname for fname in os.listdir(source_file_prefix + (topo + os.sep) +
                                                            ('r_' + str(ratio) + os.sep) + (alg + os.sep)) \
                              if not 'norm' in fname]

                combifname.sort()

                x_label_one = ['[' + item[:-4] + ']' for item in combifname if len(item[:-4].split('-')) == 1]
                x_label_two = ['[' + item[:-4].replace('-', ',') + ']' for item in combifname if len(item[:-4].split('-')) == 2]

                for combination in combifname:

                    source_file_name = source_file_prefix + (topo + os.sep) + \
                                        ('r_' + str(ratio) + os.sep) + \
                                        (alg + os.sep) + \
                                        combination
                    orig_x, x, contro_swtich, failed_switch_loc, flow_switch = read_data(source_file_name)
                    failed_switch = cal_failed_switch(orig_x)

                    outputfile_prefix = 'output' + os.sep + (topo + os.sep) + \
                                        ('r_' + str(ratio) + os.sep) + \
                                        (alg + os.sep)
                    if not os.path.exists(outputfile_prefix):
                        os.makedirs(outputfile_prefix)
                    cal_remap(failed_switch, contro_swtich, outputfile_prefix + combination + '.txt')

                    # # get failed_controller from the combination
                    # tmp_str_list = combination.split('-')
                    # failed_controller_id = [int(i) for i in tmp_str_list]
                    recov_obj = cal_recovered_object(contro_swtich, w, failed_switch)
                    norm_recov_obj = cal_recovered_object(norm_contro_swtich, w, failed_switch)

                    # obj = cal_object(contro_swtich, w)
                    sum_per, real_per = cal_recovered_flow_percentage(orig_x, x, flow_switch)
                    # convert to percentage
                    real_per *= 100.0
                    recov_switch = cal_recovered_switch(orig_x, x)

                    control_flow_list = cal_control_flownum(contro_swtich, flow_switch)
                    switch_num_list = cal_control_switch_num(contro_swtich)


                    # failed_switch_flow = cal_switchs_flow_list(failed_switch, flow_switch)
                    # live_controller = cal_live_control(norm_contro_swtich, norm_orig_x)
                    #
                    # contro_list = cal_control_flownum(norm_contro_swtich, norm_flow_switch)


                    plus_score = 0
                    if alg == 'near':

                        for item in control_flow_list:
                            if item[2] > 500:
                                tmp = item[2] - 500
                                # plus_score += ((tmp + 1) * tmp / 2.0 * 0.005)
                                plus_score += ((tmp + 1) * 0.03)

                    flows_list = []
                    for item in control_flow_list:
                        # flows_list.append(len(item[1]))
                        flows_list.append(item[2])

                    switchs_list = []
                    for item in switch_num_list:
                        switchs_list.append(item[1])


                    if norm_recov_obj == 0:
                        norm_recov_obj = 1
                        recov_obj = 1

                    xval = combination[:-4]
                    if len(xval.split('-')) == 1:
                        # ratio_object_one_list.append(recov_obj / float(norm_recov_obj))
                        ratio_object_one_list.append(recov_obj + plus_score)
                        ratio_recflow_percen_one_list.append(real_per)
                        ratio_recswitchnum_one_list.append(len(recov_switch))
                        ratio_controflownum_one_list.append(flows_list)

                        # x_label_one.append('[' + xval + ']')
                    else:
                        # ratio_object_two_list.append(recov_obj / float(norm_recov_obj))
                        ratio_object_two_list.append(recov_obj + plus_score)
                        ratio_recflow_percen_two_list.append(real_per)
                        ratio_recswitchnum_two_list.append(len(recov_switch))
                        ratio_controflownum_two_list.append(flows_list)
                        # x_label_two.append('[' + xval.replace('-', ',') + ']')

                    write_obj(recov_obj + plus_score, outputfile_prefix + 'obj' + combination)





                    xval = combination[:-4]
                    if len(xval.split('-')) == 1:
                        ratio_alg_flownum_one_dict[(combi_count, alg_count)] = flows_list
                        ratio_alg_switchNum_one_dict[(combi_count, alg_count)] = switchs_list
                    else:
                        ratio_alg_flownum_two_dict[(combi_count, alg_count)] = flows_list
                        ratio_alg_switchNum_two_dict[(combi_count, alg_count)] = switchs_list



                    combi_count += 1
                    ###########################
                    ###########################







                alg_obj_one_list.append(ratio_object_one_list)
                alg_recflow_percen_one_list.append(ratio_recflow_percen_one_list)
                alg_recswitchnum_one_list.append(ratio_recswitchnum_one_list)

                box_alg = ['GreedyAlg', 'near', 'recover']
                box_alg.sort()
                box_legend = [algname_lagend_dict[i] for i in box_alg]
                box_legend[0] += ' (Left)'
                box_legend[1] += ' (Middle)'
                box_legend[2] += ' (Right)'
                if alg in ['GreedyAlg', 'near', 'recover']:
                    alg_combi_contro_flow_num_one.append(ratio_controflownum_one_list)
                    alg_combi_contro_flow_num_two.append(ratio_controflownum_two_list)

                alg_obj_two_list.append(ratio_object_two_list)
                alg_recflow_percen_two_list.append(ratio_recflow_percen_two_list)
                alg_recswitchnum_two_list.append(ratio_recswitchnum_two_list)





                alg_count += 1
            #######################
            #######################

            # add norm
            # alg_obj_one_list.append([1 for i in range(len(alg_obj_one_list[0]))])
            # alg_obj_two_list.append([1 for i in range(len(alg_obj_two_list[0]))])

            # calculate the near ratio data vector
            # get near index
            near_index = cal_near_index(algfnames)
            alg_objovernearobj_one_list = cal_objratio_list(alg_obj_one_list, near_index)
            alg_objovernearobj_two_list = cal_objratio_list(alg_obj_two_list, near_index)

            legend = [algname_lagend_dict[i] for i in algfnames]
            dst_file_prefix = 'figure' + os.sep + source_file_prefix + os.sep

            dst_file_prefix += (topo + '-' + str(ratio) + os.sep)
            if not os.path.exists(dst_file_prefix):
                os.makedirs(dst_file_prefix)

            # simple_plot(filename=dst_file_prefix + 'obj.pdf',
            #             x_vector=ratio_list, y_vector_list=alg_obj_list,
            #             marker=['s','o','+', 'x', 'D', '^', '*'], legend=legend)
            #
            # simple_plot(filename=dst_file_prefix + 'recovPercent.pdf',
            #             x_vector=ratio_list, y_vector_list=alg_recflow_percen_list,
            #             marker=['s', 'o', '+', 'x', 'D', '^', '*'], legend=legend)
            #
            # simple_plot(filename=dst_file_prefix + 'recovSwitch.pdf',
            #             x_vector=ratio_list, y_vector_list=alg_recswitchnum_list,
            #             marker=['s', 'o', '+', 'x', 'D', '^', '*'], legend=legend)

            bar_char_pdf(filename=dst_file_prefix + 'bar-obj-one.pdf', data=alg_obj_one_list,
                         xticks=x_label_one, legend=legend+['Normal'], x_label="ID of failed controllers", y_label="Object ratio")

            bar_char_pdf(filename=dst_file_prefix + 'bar-obj-two.pdf', data=alg_obj_two_list,
                         xticks=x_label_two, legend=legend+['Normal'], x_label="ID of failed controllers", y_label="Object ratio")

            bar_char_pdf(filename=dst_file_prefix + 'bar-objratio-one.pdf', data=alg_objovernearobj_one_list,
                         xticks=x_label_one, legend=legend + ['Normal'], x_label="ID of failed controllers", y_label="Percentage to Nearest (\%)")

            bar_char_pdf(filename=dst_file_prefix + 'bar-objratio-two.pdf', data=alg_objovernearobj_two_list,
                         xticks=x_label_two, legend=legend + ['Normal'], x_label="ID of failed controllers", y_label="Percentage to Nearest (\%)")

            bar_char_pdf(filename=dst_file_prefix + 'bar-recovPercent-one.pdf', data=alg_recflow_percen_one_list,
                         xticks=x_label_one, legend=legend, x_label="ID of failed controllers", y_label="Recovered flow percentage (\%)")

            bar_char_pdf(filename=dst_file_prefix + 'bar-recovPercent-two.pdf', data=alg_recflow_percen_two_list,
                         xticks=x_label_two, legend=legend, x_label="ID of failed controllers", y_label="Recovered flow percentage (\%)")

            bar_char_pdf(filename=dst_file_prefix + 'bar-recovSwitch-one.pdf', data=alg_recswitchnum_one_list,
                         xticks=x_label_one, legend=legend, x_label="ID of failed controllers", y_label="Number of recovered switch")

            bar_char_pdf(filename=dst_file_prefix + 'bar-recovSwitch-two.pdf', data=alg_recswitchnum_two_list,
                         xticks=x_label_two, legend=legend, x_label="ID of failed controllers", y_label="Number of recovered switch")

            box_group_pdf(filename=dst_file_prefix + "contro_flow_num-one.pdf", data=alg_combi_contro_flow_num_one,
                          xtick=x_label_one, x_label="ID of failed controllers", y_label="Number of flows",
                          legend=box_legend, hline=ability)

            box_group_pdf(filename=dst_file_prefix + "contro_flow_num-two.pdf", data=alg_combi_contro_flow_num_two,
                          xtick=x_label_two, x_label="ID of failed controllers", y_label="Number of flows",
                          legend=box_legend, hline=ability)


            # for i in range(len(combifname)):
            #     ratio_alg_box_flownum_one_list = []
            #     ratio_alg_box_flownum_two_list = []
            #     ratio_alg_box_switchnum_one_list = []
            #     ratio_alg_box_switchnum_two_list = []
            #
            #     xval = combifname[i][:-4]
            #
            #     for j in range(len(algfnames)):
            #         if len(xval.split('-')) == 1:
            #             ratio_alg_box_flownum_one_list.append(ratio_alg_flownum_one_dict[(i, j)])
            #             ratio_alg_box_switchnum_one_list.append(ratio_alg_switchNum_one_dict[(i, j)])
            #         else:
            #             ratio_alg_box_flownum_two_list.append(ratio_alg_flownum_two_dict[(i, j)])
            #             ratio_alg_box_switchnum_two_list.append(ratio_alg_switchNum_two_dict[(i, j)])
            #     # add norm alg
            #     if len(xval.split('-')) == 1:
            #         ratio_alg_box_flownum_one_list.append(norm_flows_list)
            #         ratio_alg_box_switchnum_one_list.append(norm_switchs_list)
            #     else:
            #         ratio_alg_box_flownum_two_list.append(norm_flows_list)
            #         ratio_alg_box_switchnum_two_list.append(norm_switchs_list)
            #
            #     # add xtick labels
            #     alg_xtick = deepcopy(legend)
            #     alg_xtick.append('Normal')
            #
            #     # plot the two boxplot
            #     box_plot_prefix = 'figure' + os.sep + str(combifname[i]) + os.sep + dst_file_prefix + os.sep
            #     if not os.path.exists(box_plot_prefix):
            #         os.makedirs(box_plot_prefix)
            #     if len(xval.split('-')) == 1:
            #         box_pdf(box_plot_prefix + "contro_flow_num-one.pdf", data=ratio_alg_box_flownum_one_list,
            #                 xtick=alg_xtick, y_label="\# of flows")
            #         box_pdf(box_plot_prefix + "contro_switch_num-one.pdf", data=ratio_alg_box_switchnum_one_list,
            #                 xtick=alg_xtick, y_label="\# of switches")
            #     else:
            #         box_pdf(box_plot_prefix + "contro_flow_num-two.pdf", data=ratio_alg_box_flownum_two_list,
            #                 xtick=alg_xtick, y_label="\# of flows")
            #         box_pdf(box_plot_prefix + "contro_switch_num-two.pdf", data=ratio_alg_box_switchnum_two_list,
            #                 xtick=alg_xtick, y_label="\# of switches")

            print dst_file_prefix + 'done'



if __name__ == '__main__':

    main()