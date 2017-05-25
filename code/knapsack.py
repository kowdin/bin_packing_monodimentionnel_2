from instance import Instance

class Knapsack_solver:

    valeurs = None
    poids = None
    instance = None
    ind_ord = None
    capacite = None
    affect = None
    solution = 0
    nb_obj = 0
    ind = 0

    def __init__(self, instance):

        self.poids = list()
        self.ind_ord = list()
        self.instance = instance
        self.valeurs = [0.]*self.instance.nb_obj_tot
        self.ind_ord = [x for x in range(self.instance.nb_obj_tot)]
        self.capacite = self.instance.cap
        self.affect = [False]*self.instance.nb_obj_tot
        self.solution = 0.
        self.nb_obj = self.instance.nb_obj_tot
        self.ind = 0
        self.sol_var = [False]*self.nb_obj
        self.sol_relax = [False]*self.nb_obj

        for i in range(0, instance.nb_obj_diff):
            for j in range(0, instance.obj_nb[i]):
                self.poids.append(instance.obj_taille[i])

    # résolution du problème avec comme valeurs la liste val
    def resoudre(self, val):

        # valeur de la solution (partielle)
        self.solution = 0.

        # indice du sous problème à résoudre (lorsque les premières variables sont affectées)
        self.ind = 0

        # meilleures solution
        meilleure_sol = 0

        # liste des variables affectées
        for i in range(0, len(self.affect)):
            self.affect[i] = False

        # valeurs des objets
        for i in range(0, self.instance.nb_obj_tot):
            self.valeurs[i] = val[i]

        # self.afficher()

        # tri des objets par utilité
        self.ind_ord.sort(key = lambda ind: -self.valeurs[ind]/self.poids[ind])

        continuer = True

        while continuer:

            print("ind: ", self.ind)

            # relaxation linéaire du sous-problème
            (relax, opt) = self.relaxation_lineaire()
            relax += self.solution
            # print("relax: ", relax)

            # exploration si nécessaire
            if relax > meilleure_sol:

                if opt and relax > meilleure_sol:
                    meilleure_sol = relax
                    self.sol_var = list(self.sol_relax)
                    # print("amélioration (relax): ", meilleure_sol)

                if not opt:
                    # print("exploration")
                    self.exploration()

                    # mise à jour de la meilleure solution
                    if self.solution > meilleure_sol:
                        meilleure_sol = self.solution
                        self.sol_var = list(self.affect)
                        # print("amélioration: ", meilleure_sol)

            # backtracking
            if self.ind >= 1:
                self.backtracking()

            if self.ind <= 0:
                continuer = False

        return (meilleure_sol, self.sol_var)

    # backtracking dans l'arbre de branch and bound
    def backtracking(self):

        # retour vers la dernière variable affectée à 1 -> l'affecter à 0
        continuer = True

        while continuer:
            # si la dernière variables affectée à 1 est trouvée, elle est affectée à 0
            if self.affect[self.ind-1]:
                continuer = False
                self.affect[self.ind-1] = False
                self.capacite += self.poids[self.ind_ord[self.ind-1]]
                self.solution -= self.valeurs[self.ind_ord[self.ind-1]]
            else:
                self.ind -= 1

            # exploration terminée
            if self.ind <= 0:
                continuer = False


    # exploration dans l'arbre du branch and bound
    def exploration(self):

        continuer = True
        while self.ind < self.nb_obj:

            # l'objet est ajouté si il rentre
            if self.poids[self.ind_ord[self.ind]] <= self.capacite:
                self.affect[self.ind] = True
                self.capacite -= self.poids[self.ind_ord[self.ind]]
                self.solution += self.valeurs[self.ind_ord[self.ind]]

            self.ind += 1

    # relaxation linéaire du sous problèmes commençant à l'indice ind
    def relaxation_lineaire(self):

        res = 0.
        continuer = True
        ind = self.ind
        capa = self.capacite

        opt = True


        i = 0
        for elt in self.sol_relax:
            if i < ind:
                elt = self.affect[i]
            else:
                elt = False
            i += 1

        # ajout des objets qui le peuvent dans le sac
        while continuer:

            # objet ajoutés en entier dans le sac
            if self.poids[self.ind_ord[ind]] <= capa:
                capa -= self.poids[self.ind_ord[ind]]
                res += self.valeurs[self.ind_ord[ind]]
                self.sol_relax[ind] = True
                ind += 1

                # si le sac est remplie, la relaxation est terminée (et optimale)
                if capa <= 10**-6:
                    continuer = False

            else: # objet ajoutés partiellement
                prop = capa/self.poids[self.ind_ord[ind]]
                res += self.valeurs[self.ind_ord[ind]]*prop
                continuer = False
                opt = False # la relaxation n'est pas optimale

            # si tous les objets ont été ajoutés, la relaxation est terminée
            if ind >= self.nb_obj:
                continuer = False

        return (res, opt)

    # affichage du problème
    def afficher(self):
        print(self.valeurs)
        print(self.poids)
        print(self.capacite)
