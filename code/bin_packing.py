
#!/usr/bin/python

from instance import Instance
from heuristique import best_fit
from lagrange import relax_lagrange

from random import randint

from lagrange_kp2 import relax_lagrange_kp

inst = Instance("../Instances/c150/Falkenauer_u120_00.txt")
#inst = Instance("../Instances/c1000/Falkenauer_t120_03.txt")
#inst = Instance("jouet2.txt")
#inst.afficher()

print("L'heuristique best fit donne : " + str(best_fit(inst)))
print("La relaxation lineaire donne : " + str(inst.relaxation_lineaire()) )

#(val,x,u,mu,gamma) = relax_lagrange(inst)
#print("La relaxation lagrangienne donne : " + str(val))
#print("\touverture : "+str(u))
#print("\t associations : ")
#acc = 0
#for p in range(0, inst.nb_obj_diff):
#   for _ in range(0, inst.obj_nb[p]):
#       print("\t\t"+str(x[acc]))
#       acc +=1

#relax_lagrange_kp(inst)

#print("\tmu : "+str(mu))
#print("\tgamma : "+str(gamma))
# kp_solver = Knapsack_solver(inst)

# val = [0.7*(inst.nb_obj_tot-x) for x in range(0, inst.nb_obj_tot)]
# val = [2.]*inst.nb_obj_tot
#val = [inst.nb_obj_tot-x for x in range(0,inst.nb_obj_tot)]

#kp_solver.resoudre(val)

(val,x,u,mu) = relax_lagrange_kp(inst)
print("La relaxation lagrangienne donne : " + str(val))
print("\touverture : "+str(u))
print("\t associations : "+str(x))
#print("Coeficient lagrangien : "+str(mu))