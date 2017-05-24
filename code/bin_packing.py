#!/usr/bin/python

from instance import Instance
from heuristique import best_fit
from lagrange import relax_lagrange

from knapsack import Knapsack_solver

inst = Instance("../Instances/c150/Falkenauer_u250_02.txt")
#inst = Instance("jouet.txt")
#inst.afficher()

# print("L'heuristique best fit donne : " + str(best_fit(inst)))
# print("La relaxation lineaire donne : " + str(inst.relaxation_lineaire()) )
# print("La relaxation lagrangienne donne : " + str(relax_lagrange(inst)))

kp_solver = Knapsack_solver(inst)
