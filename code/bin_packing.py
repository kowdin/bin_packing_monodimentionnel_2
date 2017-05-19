#!/usr/bin/python

from instance import Instance
from heuristique import best_fit

inst = Instance("../Instances/c150/Falkenauer_u120_00.txt")
# inst.afficher()

print("L'heuristique best fit donne : " + str(best_fit(inst)))
print("La relaxation lineaire donne : " + str(inst.relaxation_lineaire()) )
