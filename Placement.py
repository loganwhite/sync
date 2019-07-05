from igraph import *
import os, math
import numpy as np
import time
from gurobipy import *

"""
    pathcandidate: the flow_path matrix, where each row means a flow id, each column is a path id
"""


class Para():
    def __init__(self, delay, flow_num, location_num, controller_loc):
        self.delay = delay  # location_num * location_num
        self.location_num = location_num
        self.controller_loc = controller_loc  # location_num


class Optimal(Para):
    def __init__(self, delay, flow_num, location_num, controller_loc):

        Para.__init__(self, delay, flow_num, location_num, controller_loc)
        self.name = "Optimal"
        self.x = []
        self.z = []
        self.res = 0
        self.normal_perf = 0

    def process(self, flow_switch, failed_switches, available_controllers, A, ratio,
                failed_total_flow_num):
        #     print("old_y ", old_y,flow_rate, link_cap, node_table)
        self.get_network_state(flow_switch, failed_switches, available_controllers, A,
                               ratio, failed_total_flow_num)
        self.math_solution()
        return self.res, self.z, self.x

    def get_network_state(self, flow_switch, failed_switches, available_controllers, A, ratio,
                          failed_total_flow_num):
        self.flow_num = failed_total_flow_num
        self.flow_switch = flow_switch  # location_num * flow_num
        self.failed_switches = failed_switches
        self.available_controllers = available_controllers
        self.A = A
        self.cur_flow_num = math.ceil(ratio * failed_total_flow_num)
        self.switch_flow_nums = self.get_switch_flow_nums()
        self.w = self.get_w()  # location_num * location_num
        self.z = [[0 for i in range(self.location_num)] for j in range(self.location_num)]
        self.x = [0 for i in range(self.location_num)]
        self.y = [0 for i in range(self.location_num)]
        self.d = [0 for i in range(self.flow_num)]

    def get_switch_flow_nums(self):
        switch_flow_nums = [0 for i in range(self.location_num)]

        np_flow_swith = np.asarray(self.flow_switch)

        np_swith_flow = np_flow_swith.transpose()
        sf = np_swith_flow.tolist()

        for i in self.failed_switches:
            switch_flow_nums[i] = sum(sf[i])

        return switch_flow_nums

    def get_w(self):
        w = [[0 for i in range(self.location_num)] for j in range(self.location_num)]
        for i in range(self.location_num):
            for j in range(self.location_num):
                sum = 0
                for l in range(self.flow_num):
                    sum += self.flow_switch[l][i]
                # print sum
                w[i][j] = sum * self.delay[i][j]
        return w

    def get_variables(self, model):
        x = model.addVars(self.location_num, vtype=GRB.BINARY, name="x")
        z = model.addVars(self.location_num, self.location_num, vtype=GRB.BINARY, name="z")
        d = model.addVars(self.flow_num, vtype=GRB.BINARY, name="d")
        return x, z, d

    def math_solution(self):
        # print("optimization starts")
        try:
            # Create a new model
            model = Model(self.name)
            model.setParam('OutputFlag', False)
            # Create variables
            x, z, d = self.get_variables(model)

            # Add constraints
            #     model.addConstrs((z[i,j] <= self.controller_loc[j]
            #         for i in self.failed_switches
            #         for j in self.available_controllers),
            #         name="default_controller_mapping_relationship")

            model.addConstrs((quicksum(z[i, j]
                                       for j in self.available_controllers) == x[i]
                              for i in self.failed_switches), name="mapping")

            model.addConstrs((quicksum(self.switch_flow_nums[i] * z[i, j]
                                       for i in self.failed_switches) <= self.A[j]
                              for j in self.available_controllers), name="controller ability")

            # model.addConstrs((quicksum(self.flow_switch[l][i] * z[i,j]
            #     for i in self.failed_switches
            #     for j in self.available_controllers) >= d[l]
            #     for l in range(self.flow_num)), name="flow programmable")

            model.addConstrs((quicksum(self.flow_switch[l][i] * x[i]
                                       for i in self.failed_switches) >= d[l]
                              for l in range(self.flow_num)), name="flow programmable")

            model.addConstr(quicksum(d[l]
                                     for l in range(self.flow_num)) >= self.cur_flow_num,
                            name="domain programmable")

            # Set objective
            model.setObjective(quicksum(self.w[i][j] * z[i, j]
                                        for i in self.failed_switches
                                        for j in self.available_controllers),
                               GRB.MINIMIZE)

            # Integrate new variables
            model.update()
            # print("solving math starts")
            self.opt_start_time = time.time()
            model.optimize()
            # print("solving math ends")
            self.opt_end_time = time.time()
            # print("solution time : %s" % (self.opt_end_time - self.opt_start_time))
            status = model.status
            print("name: %s, status = %s" % (self.name, status))
            if status == 3:
                return

            print('The optimal objective is %g\n' % model.objVal)

            if status == GRB.Status.UNBOUNDED:
                print('The model cannot be solved because it is unbounded')
                # exit(0)

            if status == GRB.Status.OPTIMAL:
                self.res = model.objVal

                # exit(0)
                for v in model.getVars():
                    if v.x == 0:
                        continue
                    string = v.varName
                    if "z" in v.varName:
                        string = string.replace("z[", "").replace("]", "")
                        strlist = string.split(',')
                        switch_id, controller_id = int(strlist[0]), int(strlist[1])
                        # print("in opti switch_id, controller_id,v.x", switch_id, controller_id,v.x)
                        self.z[switch_id][controller_id] = v.x
                        self.x[switch_id] = 1
                        # self.res.append((flow_id,path_id,v.x))
                        # print(flow_id, path_id)
                        # print(self.y[flow_id][path_id])
                        # print("z[%s][%s]=%s" %(row_num,col_num,self.z[row_num][col_num]))
                    # if "x" in v.varName:
                    #     string = string.replace("x[","").replace("]","")
                    #     self.x[int(string)] = v.x
                    if "d" in v.varName:
                        string = string.replace("d[", "").replace("]", "")
                        self.d[int(string)] = v.x
                        # print("x[%s]=%s" %(string,self.x[int(string)]))
                        continue

            elif status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
                print('Optimization was stopped with status %d' % status)
                # pass
                # exit(0)
            # print("optimization ends")
        except GurobiError:
            print ('Error reported')



class Placement(Optimal):
    # def __init__(self,total_path_num,flow_num,link_num,node_num,p_l,p_n,LB,T,OL,flow_pathcandidate,flow_path, no_loop_para):
    #     self.name = "lp"
    #     Optimal.__init__(self,total_path_num,flow_num,link_num,node_num,p_l,p_n,LB,T,OL,flow_pathcandidate,flow_path, no_loop_para)

    def __init__(self, delay, flow_num, location_num, controller_loc):

        Optimal.__init__(self, delay, flow_num, location_num, controller_loc)
        self.name = "Placement"
        self.x = []
        self.y = []
        self.z = []
        self.res = 0
        self.normal_perf = 0

    # def process(self,old_y,flow_rate,link_cap,node_table, critical_list_flow_relationship):
    #     self.get_network_state(old_y,flow_rate,link_cap,node_table, critical_list_flow_relationship)
    #     self.math_solution()

    def get_variables(self, model):
        x = model.addVars(self.location_num, vtype=GRB.BINARY, name="x")
        y = model.addVars(self.location_num, vtype=GRB.BINARY, name="y")
        z = model.addVars(self.location_num, self.location_num, vtype=GRB.BINARY, name="z")
        return z, y

    def math_solution(self):
        # print("optimization starts")
        try:
            # Create a new model
            model = Model(self.name)
            model.setParam('OutputFlag', False)
            # Create variables
            z, y = self.get_variables(model)

            # Add constraints
            model.addConstrs((quicksum(z[i, j]
                                       for j in self.available_controllers) == 1
                              for i in self.failed_switches), name="mapping0")

            # model.addConstrs((z[i, j] <= y[j]
            #                   for i in self.failed_switches
            #                   for j in self.available_controllers), name="mapping1")

            model.addConstrs((quicksum(self.switch_flow_nums[i] * z[i, j]
                                       for i in self.failed_switches) <= self.A[j] * y[j]
                              for j in self.available_controllers), name="controller ability")

            model.addConstr((quicksum(y[j]
                                      # for j in self.available_controllers) <= len(self.available_controllers)/6),
                                      for j in self.available_controllers) == 6),
                            name="controller number")

            # Set objective
            model.setObjective(quicksum(self.w[i][j] * z[i, j]
                                        for i in self.failed_switches
                                        for j in self.available_controllers),
                               GRB.MINIMIZE)

            # Integrate new variables
            model.update()
            # print("solving math starts")
            self.opt_start_time = time.time()
            model.optimize()
            # print("solving math ends")
            self.opt_end_time = time.time()
            # print("solution time : %s" % (self.opt_end_time - self.opt_start_time))
            status = model.status
            print("name: %s, status = %s" % (self.name, status))
            if status == 3:
                return

            print('The optimal objective is %g\n' % model.objVal)

            if status == GRB.Status.UNBOUNDED:
                print('The model cannot be solved because it is unbounded')
                # exit(0)

            if status == GRB.Status.OPTIMAL:
                self.res = model.objVal

                # exit(0)
                for v in model.getVars():
                    if v.x == 0:
                        continue
                    string = v.varName
                    if "z" in v.varName:
                        string = string.replace("z[", "").replace("]", "")
                        strlist = string.split(',')
                        switch_id, controller_id = int(strlist[0]), int(strlist[1])
                        # print("in opti switch_id, controller_id,v.x", switch_id, controller_id,v.x)
                        self.z[switch_id][controller_id] = v.x
                        # self.res.append((flow_id,path_id,v.x))
                        # print(flow_id, path_id)
                        # print(self.y[flow_id][path_id])
                        # print("z[%s][%s]=%s" %(row_num,col_num,self.z[row_num][col_num]))
                    if "x" in v.varName:
                        string = string.replace("x[", "").replace("]", "")
                        self.x[int(string)] = v.x
                    if "y" in v.varName:
                        string = string.replace("y[", "").replace("]", "")
                        self.y[int(string)] = v.x
                        # print("x[%s]=%s" %(string,self.x[int(string)]))
                    #     continue

            elif status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
                print('Optimization was stopped with status %d' % status)
                # pass
                # exit(0)
            # print("optimization ends")
        except GurobiError:
            print "hh"