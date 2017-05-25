#!/usr/bin/python

from instance import Instance
from heuristique import best_fit
from lagrange import relax_lagrange

from knapsack import Knapsack_solver

from random import randint

#inst = Instance("../Instances/c150/Falkenauer_u250_02.txt")
inst = Instance("jouet2.txt")
#inst.afficher()

# print("L'heuristique best fit donne : " + str(best_fit(inst)))
# print("La relaxation lineaire donne : " + str(inst.relaxation_lineaire()) )
# print("La relaxation lagrangienne donne : " + str(relax_lagrange(inst)))

kp_solver = Knapsack_solver(inst)

# val = [0.7*(inst.nb_obj_tot-x) for x in range(0, inst.nb_obj_tot)]
# val = [2.]*inst.nb_obj_tot
val = [inst.nb_obj_tot-x for x in range(0,inst.nb_obj_tot)]

kp_solver.resoudre(val)
