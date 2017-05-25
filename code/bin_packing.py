#!/usr/bin/python

from instance import Instance
from heuristique import best_fit
from lagrange import relax_lagrange

from random import randint

from lagrange_kp import relax_lagrange_kp

#inst = Instance("../Instances/c150/Falkenauer_u120_00.txt")
#inst = Instance("../Instances/c1000/Falkenauer_t120_03.txt")
inst = Instance("jouet2.txt")
#inst.afficher()

# print("L'heuristique best fit donne : " + str(best_fit(inst)))
# print("La relaxation lineaire donne : " + str(inst.relaxation_lineaire()) )
# (val,x,u,mu,gamma) = relax_lagrange(inst)
# print("La relaxation lagrangienne donne : " + str(val))
#print("\touverture : "+str(u))
#print("\t associations : ")
#acc = 0
#for p in range(0, inst.nb_obj_diff):
#   for _ in range(0, inst.obj_nb[p]):
#       print("\t\t"+str(x[acc]))
#       acc +=1

relax_lagrange_kp(inst)
