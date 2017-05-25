from instance import Instance
from heuristique import best_fit
from knapsack import Knapsack_solver

def relax_lagrange_kp(inst):

    # sous-problèmes de sac à dos
    kp_solver = Knapsack_solver(inst)

    # best fit
    nbBoite = best_fit(inst)
    print("best fit: ", nbBoite)

    # multiplicateurs
    mult = [0] * inst.nb_obj_tot
    # gradient de la fonction à maximiser
    grad = [0.] * inst.nb_obj_tot

    # solution du pb de sac à dos
    sol_kp = None

    continuer = True

    # paramètres pour les sous-gradients
    epsilon = 1.
    pas = 0.5
    rho = 0.6

    while continuer:

        # somme des multiplicateurs
        somme_mult = 0
        for elt in mult:
            somme_mult += elt

        # résolution du problème de sac à dos
        (kp_res, sol_kp) = kp_solver.resoudre(mult)

        relax = 0

        # si le résultat est > 1, alors le bin doit être utilisé
        if kp_res > 1:

            relax = (1-kp_res)*nbBoite + somme_mult
            # calcul du gradient
            for i in range(0,len(sol_kp)):
                grad[i] = 1. - nbBoite*sol_kp[i]
            # calcul du pas
            somme_x = 0
            for x in sol_kp:
                somme_x += x
            somme_x -= 1
            # pas = epsilon * ( (nbBoite-relax) / (somme_x*somme_x) )

        else:
            relax = somme_mult
            # calcul du gradient
            grad = [1.]*inst.nb_obj_tot
            # pas = epsilon * (nbBoite-relax)

        print("relaxation lagrangienne: ", relax)
        print("pas: ", pas)

        pas = pas*rho
        rho = rho*0.5

        # mise à jour des multiplicateurs
        for i in range(0, len(mult)):
            mult[i] += pas*grad[i]

        if(pas <= 10**-18):
            continuer = False
