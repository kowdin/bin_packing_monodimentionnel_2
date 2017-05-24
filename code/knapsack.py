from instance import Instance

class Knapsack_solver:

    valeurs = None
    poids = None

    def __init__(self, instance):

        valeurs = list()
        poids = list()

        for i in range(0, instance.nb_obj_diff):
            for j in range(0, instance.obj_nb[i]):
                poids.append(instance.obj_taille[i])
                valeurs.append(0)

    def resoudre(self, val):

        for i in range(0, instance.nb_obj_tot):
            valeurs[i] = val[i]

        print("test")
