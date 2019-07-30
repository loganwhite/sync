from igraph import *

import os, math

import numpy as np

import time

from gurobipy import *





"""

    pathcandidate: the flow_path matrix, where each row means a flow id, each column is a path id

"""

class Para_new():

    def __init__(self,total_path_num,flow_num,link_num,node_num,p_l,p_n,LB,TB,OL,

        flow_pathcandidate, flow_path, no_loop_para,flow_flowcandidate_path,flow_flowcandidate):

        self.total_path_num = total_path_num

        self.flow_num = flow_num

        self.link_num = link_num

        self.node_num = node_num

        self.flow_pathcandidate = flow_pathcandidate


        self.p_l = p_l # feasible path-link relation matrix, 

        # x is path index, y is link index, self.total_path_num * self.link_num

        self.p_n = p_n # feasible path-node relation matrix,  

        # x is path index, y is node index, self.total_path_num * self.node_num

        self.LB = LB

        self.TB = TB

        self.OL = OL

        

        self.flow_flowcandidate_path = flow_flowcandidate_path

        self.flow_flowcandidate = flow_flowcandidate

        # self.flow_link = self.get_flow_link()

        self.flow_path = flow_path

        self.no_loop_para = no_loop_para


        # print(self.flow_link)

        # input()

    # def get_flow_link(self):

    #     flow_link = [[0 for l in range(self.link_num)] for m in range(self.flow_num)]

    #     for m in range(self.flow_num):

    #         for l in range(self.link_num):

    #             # self.flow_link[m][l] = 0

    #             for i in range(self.total_path_num):

    #                 flow_link[m][l] += self.flow_pathcandidate[m][i] * self.p_l[i][l]

    #     return flow_link

         



class Optimal_new(Para_new):

    def __init__(self,total_path_num,flow_num,link_num,node_num,p_l,p_n,LB,TB,OL,

        flow_pathcandidate,flow_path, no_loop_para,flow_flowcandidate_path, flow_flowcandidate):

        self.name = "Optimal"

        Para_new.__init__(self,total_path_num,flow_num,link_num,node_num,p_l,p_n,LB,TB,OL,

            flow_pathcandidate,flow_path, no_loop_para,flow_flowcandidate_path, flow_flowcandidate)

        # print("parameters",Para.__dict__)

        # self.total_path_num = total_path_num

        # self.flow_num = flow_num

        # self.link_num = link_num

        # self.node_num = node_num

        # self.p_l = p_l # feasible path-link relation matrix, x is path index, y is link index

        # # self.total_path_num * self.link_num

        # self.p_n = p_n # feasible path-node relation matrix, x is path index, y is node index

        # # self.total_path_num * self.node_num

        # self.LB = LB

        # self.T = T

        # self.OL = OL



        self.old_y = None

        self.r = []

        self.link_c = []
        self.node_table = []
        self.y = []
        self.res = []



    """

        old_y: the original path 

        flow_rate: traffic vector matrix

        link_cap: current link traffic vector

        node_table: current flow table usage vector

        return: a tuple list where each tuple is in (flow_id, path_id, value) format

    """

    def process(self,old_y,flow_rate,link_cap,critical_list_flow_relationship):

    #     print("old_y ", old_y,flow_rate, link_cap, node_table)

        self.get_network_state(old_y,flow_rate,link_cap,critical_list_flow_relationship)

        self.math_solution()



        return self.res, self.y



    def get_network_state(self,old_y,flow_rate,link_cap,critical_list_flow_relationship):

        self.old_y = old_y # old_y path selection matrix, 

        # x is flow index, y is path index, 

        # self.flow_num * self.total_path_num

        self.flow_rate = flow_rate # flow_rate, self.flow_num

        self.link_cap = link_cap # link utilization vector, self.link_num

        # self.node_table = node_table #flow table utilization vector, self.node_num

        self.critical_flows = critical_list_flow_relationship

        self.res = []


        self.y = [[[0 for i in range(self.total_path_num)] for m in range(self.flow_num)] for k in range(self.flow_num)]

    

    def get_variables(self,model):

        # x = m.addVars(self.flow_num, vtype=GRB.BINARY, name="x")

        y = model.addVars(self.flow_num, self.flow_num,

            self.total_path_num, vtype=GRB.BINARY, name="y")

        # max_value = model.addVar( name="max_value")

        r = model.addVar( name="r")

        return y, r



    def math_solution(self):

        # print("optimization starts")

        try:

        # Create a new model

            model = Model(self.name)

            model.setParam( 'OutputFlag', False ) 

        # Create variables

            y, r = self.get_variables(model)

        

        # Add constraints

        # critical flow: m, candidate flows for a critical flow: k, path: i, link: l, node: n, 

            model.addConstrs((quicksum(y[m, k, i] * self.flow_pathcandidate[k][i]
                                       * self.flow_flowcandidate_path[m][k][i]
                for k in self.flow_flowcandidate[m]
                for i in self.flow_path[k]) == 1
                for m in self.critical_flows), name="path")



            # self.flow_link[m][l] = self.flow_pathcandidate[m][i] * self.p_l[i][l]

            model.addConstrs((quicksum(y[m, k, i] * self.p_l[i][l]  * self.flow_rate[m]

                for m in self.critical_flows

                for k in self.flow_flowcandidate[m]

                for i in self.flow_path[k])

                + self.link_cap[l] <= r * self.LB[l] 

                for l in range(self.link_num)), name="link")



            # model.addConstrs((quicksum(self.p_n[i][n] * (y[m,i]* self.flow_pathcandidate[m][i] - self.old_y[m][i]) 

            #     for m in self.critical_flows

            #     for i in range(self.total_path_num)) 

            #     + self.node_table[n] <= self.TB

            #     for n in range(self.node_num)),name="table")



            # model.addConstr((quicksum(self.p_n[i][n] * (y[m,i]* self.flow_pathcandidate[m][i] + self.old_y[m][i]) 

            #     for n in range(self.node_num) 

            #     for m in self.critical_flows

            #     for i in range(self.total_path_num))<= self.OL),name="controller load")



            # model.addConstrs((max_value >= 

            #     quicksum(y[m,i] * self.p_l[i][l] * self.flow_rate[m] 

            #         for m in range(self.flow_num)

            #         for i in self.flow_path[m]) 

            #         + self.link_cap[l]  

            #         for l in range(self.link_num)),name="min_max")



            # Set objective

            

            model.setObjective(r, GRB.MINIMIZE)   

            

            # Integrate new variables

            model.update()

            # print("solving math starts")

            self.opt_start_time = time.time()

            model.optimize()

            # print("solving math ends")

            self.opt_end_time = time.time()

            print("solution time : %s" % (self.opt_end_time - self.opt_start_time))

            status = model.status

            print("status = %s" %status)

            if status == GRB.Status.UNBOUNDED:

                print('The model cannot be solved because it is unbounded')

                # exit(0)

            if status == GRB.Status.OPTIMAL:

                # print('The optimal objective is %g' % m.objVal)

                # exit(0)

                for v in model.getVars():

                    if v.x == 0:

                        continue

                    string = v.varName

                    if "y" in v.varName:

                        string = string.replace("y[","").replace("]","")

                        strlist = string.split(',')

                        flow_id, new_flow_id, path_id = \
                            int(strlist[0]), int(strlist[1]),int(strlist[2])

                        # print("in opti flow_id, path_id", flow_id, path_id)

                        self.y[flow_id][new_flow_id][path_id] = v.x

                        self.res.append((flow_id,new_flow_id,path_id,v.x))

                        # print(flow_id, path_id)

                        # print(self.y[flow_id][path_id])

                        # print("z[%s][%s]=%s" %(row_num,col_num,self.z[row_num][col_num]))

                    # if "x" in v.varName:

                    #     string = string.replace("x[","").replace("]","")

                    #     self.x[int(string)] = v.x

                    #     # print("x[%s]=%s" %(string,self.x[int(string)]))

                    #     continue



            if status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:

                print('Optimization was stopped with status %d' % status)

                # pass

                # exit(0)

            # print("optimization ends")

        except GurobiError:

            print ('Error reported')



class LP_new(Optimal_new):

    def __init__(self,total_path_num,flow_num,link_num,node_num,p_l,p_n,LB,T,OL,

        flow_pathcandidate,flow_path, no_loop_para,flow_flowcandidate_path,flow_flowcandidate):

        self.name = "lp"

        Optimal_new.__init__(self,total_path_num,flow_num,link_num,node_num,p_l,p_n,LB,T,OL,

            flow_pathcandidate,flow_path, no_loop_para,flow_flowcandidate_path,flow_flowcandidate)



    def process(self,old_y,flow_rate,link_cap,node_table, critical_list_flow_relationship):

        self.get_network_state(old_y,flow_rate,link_cap,node_table, critical_list_flow_relationship)

        self.math_solution()



    def get_variables(self,model):

        # x = m.addVars(self.flow_num, lb=0, ub=1, vtype=GRB.CONTINUOUS, name="x")

        y = model.addVars(self.flow_num, self.total_path_num, 

            lb=0, ub=1, vtype=GRB.CONTINUOUS, name="y")

        max_value = model.addVar( name="max_value")

        return y, max_value