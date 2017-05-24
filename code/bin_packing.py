#!/usr/bin/python

from instance import Instance
from heuristique import best_fit
from lagrange import relax_lagrange

#inst = Instance("../Instances/c150/Falkenauer_u120_00.txt")
inst = Instance("jouet.txt")
#inst.afficher()

print("L'heuristique best fit donne : " + str(best_fit(inst)))
print("La relaxation lineaire donne : " + str(inst.relaxation_lineaire()) )
print("La relaxation lagrangienne donne : " + str(relax_lagrange(inst)))
