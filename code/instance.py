import math

class Instance:

    cap = 0
    nb_obj = 0
    # premier formatage des données
    obj_taille = list()
    obj_nb = list()

    def __init__(self, chaine):
        self.obj_taille = list()
        self.obj_nb = list()
        self.charger(chaine)

    def charger(self, chaine):

        file = open(chaine, 'r')

        # nombre de lignes pour les objets
        nb_ligne = int(file.readline())

        # capacité des boîtes
        self.cap = int(file.readline())

        # objets
        self.nb_obj = 0
        for ligne in range(0,nb_ligne):

            taille = int(file.readline())

            if self.nb_obj == 0 or self.obj_taille[self.nb_obj-1] != taille:
                self.obj_taille.append(taille)
                self.obj_nb.append(1)
                self.nb_obj += 1
            else:
                self.obj_nb[self.nb_obj-1] += 1

        file.close()

    def afficher(self):
        print("Capacités des boîtes : " + str(self.cap))
        print("Nombre d'objets different: " + str(self.nb_obj))
        print("Nombre d'objets : "+str(sum(self.obj_nb)))
        for obj in range(1,self.nb_obj):
            print("Objet #" + str(obj) + " : t = " + str(self.obj_taille[obj]) + " ; nb = " + str(self.obj_nb[obj]))

    def relaxation_lineaire(self):
        acc = 0
        for i in range(1,self.nb_obj):
            acc += self.obj_nb[i] * self.obj_taille[i]
        return math.ceil(acc/self.cap)

